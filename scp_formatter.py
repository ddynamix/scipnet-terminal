from blessed import Terminal
import re

term = Terminal()

def format_bold(text: str):
    return re.sub(r'\*\*(.*?)\*\*', r'{term.black_on_snow3}\1{term.normal}', text)


def clean_brackets(text: str):
    # Handle triple brackets for SCP links - convert to color format
    text = re.sub(r'\[\[\[(.*?)\]\]\]', r'{term.black_on_firebrick}\1{term.normal}', text)

    # remove regular double brackets and their content
    text = re.sub(r'\[\[(.*?)\]\]', '', text)

    # remove multiline double bracketed text
    if text[0:2] == "[[" or text[-2:] == "]]":
        text = ""

    return text


def format_separator_line(line):
    # Check if line consists only of 2 or more hyphens and nothing else
    if line.strip() and all(char == '-' for char in line.strip()):
        if len(line.strip()) >= 2:
            # Return a line of '=' that spans the full terminal width
            return f"\n\n{term.grey_reverse}" + '=' * term.width + f"{term.normal}\n\n"
    return line


def clean_arrow(text: str):
    if text.strip() == ">":
        return "\n"
    return text


def formatted_print(metadata: str, scp: str):
    lines = scp.split("\n")
    lines = [x for x in lines if x.strip()]

    for line in lines:
        # End of article
        if "[[footnoteblock]]" in line:
            break

        # Remove all meta-elements of the page
        line = clean_brackets(line)

        # Bold any double-asterisked text
        line = format_bold(line)
        
        # Format any section break
        line = format_separator_line(line)
        
        # Clean all logs with empty lines
        line = clean_arrow(line)

        print(line.format(term=term) + "\n",)
