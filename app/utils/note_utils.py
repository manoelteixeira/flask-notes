# file: app/utils/note_utils.py

def generate_title(content:str):
    if content[0] == '#':
        eol = content.find('\n')
        return content[1:eol]
    words = content.strip().split()
    if len(words)  <= 4:
        return content.strip()
    else:
        return f'{" ".join(words[0:4])} ...'
    