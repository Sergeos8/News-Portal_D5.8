from django import template
import re

register = template.Library()


@register.filter()
def censor(value):
    for repl in ["наглецы", "ушлепки", "прохрюкать", "еханый", "охуительно"]:
        repl = "(" + repl[:1] + ")" + repl[1:-1] + "(" + repl[-1:] + ")"
        value = re.sub(repl, '\\1**\\2', value, flags=re.IGNORECASE)

    return f'{value}'
