# file: app/utils/note_utils.py

def generate_title(content:str):
    words = content.strip().split()
    if len(words)  <= 4:
        return content.strip()
    else:
        return f'{" ".join(words[0:4])} ...'
    