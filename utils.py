import re

LIST_PANGGILAN = ["bapak", "bapa", "bpk", "ibu", "bu"]

def clear_name(word):
    if word in LIST_PANGGILAN:
        return False
    elif "(" in word:
        return False
    elif word.isalpha():
        return False
    return True

def strip_name(name):
    name = name.lower()
    name = name.split("/")[0]
    name = name.split(" atau ")[0]
    name = name.replace(".", " ")
    name = ' '.join(name.split())
    name = re.sub('\(\s*(.*?)\s*\)', r'(\1)', name)
    name = re.sub(r"(\S)\(", r'\1 (', name)
    name = name.split(" ")
    name = [word for word in name if clear_name(word)]
    name = name.strip()
    return name