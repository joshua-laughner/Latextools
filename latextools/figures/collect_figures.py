import argparse
import re

from .. import utils

import pdb

default_pattern = 'Fig{num}'


def iter_figures(tex_file, require_label=False, figure_envs=['figure', 'figure*']):
    # Look for figure or figure* environments, within those environments try to find the
    # \includegraphics command and the \label command. Return the path to the image file
    # from the \includegraphics command and use the label to look up the figure number.
    # If can't find label, either guess the figure number or error.
    curr_fig = 1
    re_flags = re.DOTALL

    with open(tex_file, 'r') as fobj:
        text = utils.strip_comments(fobj.read())

    fig_envs_re = '|'.join([re.escape(e) for e in figure_envs])
    # This is a very complicated re. We want to look for \begin{figure} ... \end{figure},
    # or \begin{figure*} ... \end{figure*}, etc. but require that the begin and end match,
    # i.e. don't allow \begin{figure} \end{figure*}. So:
    #   \\begin\{({figenvs})\} == \\begin\{(figure|figure*)\} in normal cases: search for
    #       the next \begin of an environment
    #
    #   \\end\{\1\} match the \end command that corresponds to the \begin command; \1 references
    #       the first group, which will be the part in parentheses in the \begin regex
    #
    #   .+? non-greedy search for any character (with at least 1) between the begin and end
    figure_re = r'\\begin\{(' + fig_envs_re + ')\}.+?\\end\{\\1\}'
    pdb.set_trace()
    for match in re.finditer(figure_re, text, flags=re_flags):
        # Remove the \begin and \end parts. I didn't use look-ahead/look-behind before because
        # those don't work with variable length values. The first } should be at the end of the \begin
        # and since we do a greedy match, looking ahead for \end should get everything up to the \end{figure}.
        env_internal = re.search(r'(?<=\}).+(?=\\end)', match.group(), flags=re_flags).group()
        graphics_path = None
        label = None
        for cmd, arg in utils.iter_latex_commands(env_internal):
            if cmd == '\includegraphics':
                pass
            elif cmd == '\label':
                label = arg


def driver(tex_file, output_dir, filename_pattern=default_pattern, require_label=False):
    pass


def parse_args(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser()
        am_i_main = True
    else:
        am_i_main = False

    parser.add_argument('tex_file', help='The .tex file to search for figures.')
    parser.add_argument('output_dir', help='The directory to place the copies of figures into. Will create this '
                                           'directory if needed, but the parent directory must exist.')
    parser.add_argument('-p', '--filename-pattern', default=default_pattern,
                        help='The pattern to use when naming the copies of the figure files, without '
                             'the extension. Default is %(default). Can use the Python new-style format '
                             'specifier "num" to insert the figure number.')
    parser.add_argument('-l', '--require-label', action='store_true',
                        help='This program tries to get figure numbers (to name the copies) by looking up '
                             'the figure labels in the .aux file. If it cannot find a label, it will guess '
                             'the number of the figure, assuming sequential numbering from 1 through the file. '
                             'Setting this flag will cause it to error if it cannot find a label instead. '
                             'Use this if your figures are not labeled 1, 2, 3,...')

    if am_i_main:
        return vars(parser.parse_args())
    else:
        parser.set_defaults(driver_fxn=driver)


def main():
    args = parse_args()
    driver(**args)


if __name__ == '__main__':
    main()
