import re

def _format_tags(arg, tag):
    # Assume that the closing tag is the first word in the opening tag but with a leading slash. This way anything more
    # complicated, like <span class="something"> will get the proper closing tag </span>
    tag_word = re.search('\w+', tag)
    closing_tag = '</{}>'.format(tag_word.group())
    return '{}{}{}'.format(tag, arg, closing_tag)

def _format_chem(arg):
    html_rep = arg
    for m in re.finditer('_\d+', arg):
        html_rep = html_rep.replace(m.group())

# Create (for now) a dictionary mapping latex commands to a function that, given the argument of the command, would
# format it in HTML
latex2html_dict = {r'\textbf': lambda x: _format_tags(x, '<strong>'),
              r'\emph': lambda x: _format_tags(x, '<i>')}

