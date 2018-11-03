import os
import re

from .latex2html import latex2html_dict

import pdb


# use a raw string to avoid excessive escaping. This will look for a backslash followed by letters and possibly
# spaces then an opening curly brace.
latex_command_re_str = r'\\[a-zA-Z]+?\s*{'
latex_command_re = re.compile(latex_command_re_str)


def parse_aux_file(aux_file_name):
    _, ext = os.path.splitext(aux_file_name)
    if ext != '.aux' and not os.path.isfile(aux_file_name):
        aux_file_name += '.aux'

    labels = []

    label_re = re.compile(re.escape('\\newlabel'))

    with open(aux_file_name, 'r') as aux_obj:
        for line in aux_obj:
            if label_re.match(line) is not None:
                labels.append(_parse_label_def(line))

    return {'labels': labels}


def latex_to_html(latex_string):
    """
    Converts a string with latex commands to one formatted with HTML.
    :param latex_string: the string to convert
    :return: the HTML encoded string
    """

    # For now, this is going to be very manual, as in I will just define manually a mapping from latex commands to HTML
    # tags. A better way would be to use the XML character reference I found once, but implementing that will take some
    # time.
    html_string = latex_string
    for cmd, arg in iter_latex_commands(latex_string):
        html_representation = latex2html_dict[cmd](arg)
        html_string = html_string.replace('{}{{{}}}'.format(cmd, arg), html_representation, 1)

    return html_string


def iter_latex_commands(latex_string):
    """
    Iterate through the latex commands in a string.
    :param latex_string: the string to process
    :return: the command (including the backslash) and the argument as strings.
    """
    for match in latex_command_re.finditer(latex_string):
        arg_idx = match.group().index('{')
        string_idx = arg_idx + match.start()
        command = match.group()[:arg_idx]
        arg, _ = _group_inside_delimiter(latex_string[string_idx:])  # assume that the last character is always the ending curly brace
        yield command, arg


def strip_comments(latex_str):
    """
    Remove commented parts of a latex text.

    Takes in a string of Latex, and returns it with everything between a non-escaped % and a newline removed
    (the newline is retained).

    :param latex_str: the string of Latex to strip comments from
    :type latex_str: str

    :return: latex_str with comments removed
    :rtype: str
    """
    latex_str = re.sub(r'^%')
    return re.sub(r'(?<=[^\\])%.*?(?=\n)', '', latex_str)


def _parse_label_def(aux_file_line):
    if not aux_file_line.startswith('\\newlabel'):
        raise ValueError('Cannot parse a label definition from a string that does not start with "\\newlabel"')
    else:
        aux_file_line = re.sub(re.escape('\\newlabel'), '', aux_file_line)

    parsed_list = _parse_latex_groups(aux_file_line)

    # This assumes a line with the form:
    #
    #   {label name}{{ref string}{pageref string}{link text}{link destination}{}}
    #
    # e.g.
    #
    #   {sec: methods: vcd - calc}{{2.1}{3}{\chem{NO_2} VCD calculation}{subsection.2.1}{}}
    #
    # Note that this may not be true if the hyperref package is not loaded so this may need modified later to account
    # for that case.

    return {'label': parsed_list[0], 'ref': parsed_list[1][0], 'pageref': parsed_list[1][1],
            'link_text': parsed_list[1][2], 'link_target': parsed_list[1][3]}


def _parse_latex_groups(latex_string):
    # This function will be called recursively, so if there's no opening braces we need an escape case. Stop if there
    # are no opening braces that are not part of commands.
    if '{' not in latex_command_re.sub('', latex_string):
        return latex_string

    groups = []
    current_idx = 0
    while current_idx < len(latex_string):
        # Search for each instance of opening curly braces. If it is part of a command, do nothing special, but if it is
        # not part of a command, then split out the contained piece as a group
        if latex_string[current_idx] != '{':
            current_idx += 1
            continue

        group_substring, n_chars_in_group = _group_inside_delimiter(latex_string[current_idx:])
        current_idx += n_chars_in_group
        if re.search(latex_command_re_str + '$', latex_string[:current_idx + 1]) is None:
            groups.append(_parse_latex_groups(group_substring))

    return groups


def _group_inside_delimiter(latex_string, delimiter='{}'):
    if len(delimiter) != 2:
        raise ValueError('delimiter must have two characters, the opening and closing delimiter')

    unmatched_opening_delimiters = 0
    found_first_delimiter = False
    delimited_group = ''
    for idx, char in enumerate(latex_string):
        if found_first_delimiter:
            delimited_group += char

        if char == delimiter[0]:
            unmatched_opening_delimiters += 1
            found_first_delimiter = True
        elif char == delimiter[1]:
            unmatched_opening_delimiters -= 1

        if found_first_delimiter and unmatched_opening_delimiters == 0:
            return delimited_group[:-1], idx + 1