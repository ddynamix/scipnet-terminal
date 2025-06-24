from blessed import Terminal
import re

term = Terminal()

def clean_brackets(text: str):
    # First handle triple brackets - convert to color format
    text = re.sub(r'\[\[\[(.*?)\]\]\]', r'{term.firebrick}\1{term.normal}', text)

    # Then remove regular double brackets and their content
    text = re.sub(r'\[\[(.*?)\]\]', '', text)

    return text


def formatted_print(metadata, scp: str):
    lines = scp.split("<\p>")
    for line in lines:
        # Remove all meta-elements of the page
        line = clean_brackets(line)

        # Bold any double-astrixed text
        line = re.sub(r'\*\*(.*?)\*\*', r'{term.black_on_firebrick}\1{term.normal}', line)

        print(line.format(term=term))
