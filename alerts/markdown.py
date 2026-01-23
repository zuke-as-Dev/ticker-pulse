import re

def escape_md(text: str) -> str:
    if not text:
        return ""
    return re.sub(r'([_*$begin:math:display$$end:math:display$()~`>#+\-=|{}.!])', r'\\\1', text)
