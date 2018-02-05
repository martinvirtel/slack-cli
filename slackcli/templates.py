#! /home/martin/.virtualenvs/lambdascraper/bin/python3
from jinja2 import Environment,PackageLoader,FunctionLoader




def fileloader(filename) :
    with open(filename) as f :
        return "".join((a for a in f.read()))



compiler  = Environment(loader=FunctionLoader(fileloader),
           )


class Template:

    edit_message=compiler.from_string("""
# -----------------------------------------------------------------Do not change these!
ts: '{{message.ts}}'
channel: '{{channel}}'
#-------------------------------------------------------------------------------------

text: '{{message.text}}'

{% if message.attachments %}
{{ message.attachments_yaml }}
{% else %}
# No Attachments. To add one, uncomment this block.
{% endif %}

""")



