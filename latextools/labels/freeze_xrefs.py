import argparse
import os
import re

from .. import utils


import pdb

ref_re = re.compile(r'\\ref\{.+?\}')
pageref_re = re.compile(r'\\pageref\{.+?\}')


def find_external_files(tex_file):
    xr_re = re.compile(r'(?<=\\externaldocument\{).+(?=\})')
    external_docs = []
    tex_path = os.path.dirname(tex_file)
    with open(tex_file, 'r') as tex:
        for line in tex:
            m = xr_re.search(line)
            if m is not None:
                # If the external document is not an absolute path, then make it such, relative to the tex document.
                ex_doc = m.group()
                if not os.path.isabs(ex_doc):
                    ex_doc = os.path.abspath(os.path.join(tex_path, ex_doc))

                external_docs.append(ex_doc)

    return external_docs


def list_available_labels(external_docs):
    labels = []
    for doc in external_docs:
        aux_data = utils.parse_aux_file(doc)
        labels += aux_data['labels']

    return labels


def replace_labels_in_line(line, re_obj, labels_dict, retain_ref=True):
    for ref in re_obj.finditer(line):
        ref_id, _ = utils._group_inside_delimiter(ref.group())
        if ref_id in labels_dict.keys():
            print('Replaced "{}" with "{}"'.format(ref.group(), labels_dict[ref_id]))
            if retain_ref:
                new_str = '{}%{}\n'.format(labels_dict[ref_id], ref_id)
            else:
                new_str = labels_dict[ref_id]
            line = line.replace(ref.group(), new_str)
    return line


def replace_external_refs(tex_file_in, tex_file_out, labels, retain_ref=True):
    ref_dict = {el['label']: el['ref'] for el in labels}
    pageref_dict = {el['label']: el['pageref'] for el in labels}

    with open(tex_file_in, 'r') as reader, open(tex_file_out, 'w') as writer:
        for line in reader:
            line = replace_labels_in_line(line, ref_re, ref_dict, retain_ref=retain_ref)
            line = replace_labels_in_line(line, pageref_re, pageref_dict, retain_ref=retain_ref)
            writer.write(line)


def parse_args():
    parser = argparse.ArgumentParser(description='Replace external document cross references with static text.')
    parser.add_argument('tex_file', help='The .tex file to freeze external cross references in')
    parser.add_argument('-k', '--keep-refs', action='store_true', help='Keep previous references commented out in the .tex file')

    return parser.parse_args()


def main():
    args = parse_args()
    tex_file_in = args.tex_file
    tex_file_out = tex_file_in.replace('.tex', '-xrfrozen.tex')
    ex_files = find_external_files(tex_file_in)
    labels = list_available_labels(ex_files)
    replace_external_refs(tex_file_in, tex_file_out, labels, retain_ref=args.keep_refs)


if __name__ == '__main__':
    main()
