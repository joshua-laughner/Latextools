import re

_latex_divisions = ('part', 'chapter', 'section', 'subsection', 'subsubsection', 'paragraph', 'subparagraph')


class LatexFormatError(Exception):
    pass

def _extract_doc(file_object):
    text = file_object.read()
    match = re.search(r'(?<=\\begin\{document\}).+(?=\\end\{document\})', text)
    if match is None:
        raise LatexFormatError('Could not find \\begin{document} and \\end{document}')
    else:
        return match.group()


def _iter_sections(text):
    section_name = '(unnamed)'