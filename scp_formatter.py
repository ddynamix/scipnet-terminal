from blessed import Terminal
import re

term = Terminal()

def clean_brackets(text: str):
    # Handle triple brackets for SCP links - convert to color format
    text = re.sub(r'\[\[\[(.*?)\]\]\]', r'{term.firebrick}\1{term.normal}', text)

    # remove regular double brackets and their content
    text = re.sub(r'\[\[(.*?)\]\]', '', text)

    # remove multiline double bracketed text
    if text[0:2] == "[[" or text[-2:] == "]]":
        text = ""

    return text


def formatted_print(metadata, scp: str):
    lines = scp.split("\n")
    lines = [x for x in lines if x.strip()]

    for line in lines:
        # End of article
        if "[[footnoteblock]]" in line:
            break

        # Remove all meta-elements of the page
        line = clean_brackets(line)

        # Bold any double-astrixed text
        line = re.sub(r'\*\*(.*?)\*\*', r'{term.black_on_firebrick}\1{term.normal}', line)

        print(line.format(term=term) + "\n")
