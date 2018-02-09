#! /home/martin/.virtualenvs/lambdascraper/bin/python3
from jinja2 import Environment,PackageLoader,FunctionLoader




def fileloader(filename) :
    with open(filename) as f :
        return "".join((a for a in f.read()))



compiler  = Environment(loader=FunctionLoader(fileloader),
           )


class Template:

    edit_message=compiler.from_string("""
# type: {{ctype}} ------------------------------------------------Do not change these!
ts: '{{message.ts}}'
channel: '{{channel}}'
#-------------------------------------------------------------------------------------

text: '{{message.text}}'
parse: none # remove to auto-link @names, #channels, http://urls


{% if message.attachments %}
{{ message.attachments_yaml }}
#
# template for new attachment:
{% else %}
# No Attachments. To add one, uncomment and edit this block.
# attachments:
{% endif %}
# - author_name: 'Bobby Tables'
#   text: 'Attachment 2 - '
#   pretext: 'Pretext von Attachment 2 - '
#   title: 'Slack API Documentation'
#   footer: 'Slack API'
#   title_link: https://api.slack.com/
#   author_link: http://flickr.com/bobby/
#   footer_icon: https://platform.slack-edge.com/img/default_application_icon.png
#   ts: 123456789
#   color: a64f36
#   fields:
#   - title: 'Priority'
#     value: 'High'
#     short: false
#   fallback: 'Required plain-text summary of the attachment.'
#
#
#
#
# ---------------------------------------------- Emoji List ----
# :dpa_antwort:	https://emoji.slack-edge.com/T09LQNVSP/dpa_antwort/7af9007ea9bb818d.png
# :dpa_material:	https://emoji.slack-edge.com/T09LQNVSP/dpa_material/8c884ce656928adf.png
# :dpa_tendenz_unsicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_unsicher/bf605b38f539ebde.png
# :dpa_abschluss_verifikation:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation/5ecbcc5c4c8dc36c.png
# :dpa_tendenz_wahr:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_wahr/a20e1c1cdc113bd0.png
# :dpa_angelegenheit_unsicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_unsicher/0f930e11450ba0c2.png
# :dpa_abschluss_verifikation_ungeloest:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_ungeloest/6f3c57539c9e0f39.png
# :dpa_abschluss_verifikation_wahr:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_wahr/aff509a22fa60fd9.png
# :dpa_angelegenheit_erschrocken:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_erschrocken/f548aa2bbf6a49f9.png
# :dpa_update:	https://emoji.slack-edge.com/T09LQNVSP/dpa_update/08ddf1d64fa1673e.png
# :dpa_tendenz:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz/9f82bdd66657e137.png
# :dpa_angelegenheit_besorgt:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_besorgt/209f22f75a899a25.png
# :dpa_tendenz_falsch:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_falsch/dec6981f42004276.png
# :dpa_abschluss_verifikation_falsch:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_falsch/a892f9de7ec7ba42.png
# :dpa_verantwortlicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_verantwortlicher/011f90039fc8d933.png
# :dpa_aktivitaet:	https://emoji.slack-edge.com/T09LQNVSP/dpa_aktivitaet/9960ad5d96aa37ef.png
# :dpa_daniel:	https://emoji.slack-edge.com/T09LQNVSP/dpa_daniel/d26738e945c4215b.jpg
# :dpa_froben:	https://emoji.slack-edge.com/T09LQNVSP/dpa_froben/12cc48dd1bc5c728.jpg
# :dpa_roland:	https://emoji.slack-edge.com/T09LQNVSP/dpa_roland/7fa3bd8d9936e4c1.jpg
# :dpa_stefan:	https://emoji.slack-edge.com/T09LQNVSP/dpa_stefan/c4b0c5b559a854a8.jpg
# :dpa_dots:	https://emoji.slack-edge.com/T09LQNVSP/dpa_dots/8e3f43757035bcf7.png
#

""")



    create_message=compiler.from_string("""
# type: {{ctype}} ------------------------------------------------Do not change this!
channel: '{{channel}}'
#-------------------------------------------------------------------------------------


username: 'dpa newsdesk'
# icon_url: '{{ message.icon_url }}'
# icon_emoji: ':dpa_dots:'
text: '{{message.text}}'
parse: none # remove to auto-link @names, #channels, http://urls


# To add attachments, pleasee, uncomment and edit this block.
# attachments:
# - author_name: 'Bobby Tables'
#   text: 'Attachment 2 - '
#   pretext: 'Pretext von Attachment 2 - '
#   title: 'Slack API Documentation'
#   footer: 'Slack API'
#   title_link: https://api.slack.com/
#   author_link: http://flickr.com/bobby/
#   footer_icon: https://platform.slack-edge.com/img/default_application_icon.png
#   ts: 123456789
#   color: a64f36
#   fields:
#   - title: 'Priority'
#     value: 'High'
#     short: false
#   fallback: 'Required plain-text summary of the attachment.'
#
#
#
#
# ---------------------------------------------- Emoji List ----
# :dpa_antwort:	https://emoji.slack-edge.com/T09LQNVSP/dpa_antwort/7af9007ea9bb818d.png
# :dpa_material:	https://emoji.slack-edge.com/T09LQNVSP/dpa_material/8c884ce656928adf.png
# :dpa_tendenz_unsicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_unsicher/bf605b38f539ebde.png
# :dpa_abschluss_verifikation:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation/5ecbcc5c4c8dc36c.png
# :dpa_tendenz_wahr:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_wahr/a20e1c1cdc113bd0.png
# :dpa_angelegenheit_unsicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_unsicher/0f930e11450ba0c2.png
# :dpa_abschluss_verifikation_ungeloest:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_ungeloest/6f3c57539c9e0f39.png
# :dpa_abschluss_verifikation_wahr:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_wahr/aff509a22fa60fd9.png
# :dpa_angelegenheit_erschrocken:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_erschrocken/f548aa2bbf6a49f9.png
# :dpa_update:	https://emoji.slack-edge.com/T09LQNVSP/dpa_update/08ddf1d64fa1673e.png
# :dpa_tendenz:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz/9f82bdd66657e137.png
# :dpa_angelegenheit_besorgt:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_besorgt/209f22f75a899a25.png
# :dpa_tendenz_falsch:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_falsch/dec6981f42004276.png
# :dpa_abschluss_verifikation_falsch:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_falsch/a892f9de7ec7ba42.png
# :dpa_verantwortlicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_verantwortlicher/011f90039fc8d933.png
# :dpa_aktivitaet:	https://emoji.slack-edge.com/T09LQNVSP/dpa_aktivitaet/9960ad5d96aa37ef.png
# :dpa_daniel:	https://emoji.slack-edge.com/T09LQNVSP/dpa_daniel/d26738e945c4215b.jpg
# :dpa_froben:	https://emoji.slack-edge.com/T09LQNVSP/dpa_froben/12cc48dd1bc5c728.jpg
# :dpa_roland:	https://emoji.slack-edge.com/T09LQNVSP/dpa_roland/7fa3bd8d9936e4c1.jpg
# :dpa_stefan:	https://emoji.slack-edge.com/T09LQNVSP/dpa_stefan/c4b0c5b559a854a8.jpg
# :dpa_dots:	https://emoji.slack-edge.com/T09LQNVSP/dpa_dots/8e3f43757035bcf7.png
#

""")


    create_reply=compiler.from_string("""
# type: {{ctype}} ------------------------------------------------Do not change this!
channel: '{{channel}}'
#-------------------------------------------------------------------------------------


username: 'dpa newsdesk'
# icon_url: '{{ message.icon_url }}'
# icon_emoji: ':dpa_dots:'
text: '{{message.text}}'
thread_ts: {{ message.ts }}
text: '{{message.text}}'
parse: none # remove to auto-link @names, #channels, http://urls


# To add attachments, pleasee, uncomment and edit this block.
# attachments:
# - author_name: 'Bobby Tables'
#   text: 'Attachment 2 - '
#   pretext: 'Pretext von Attachment 2 - '
#   title: 'Slack API Documentation'
#   footer: 'Slack API'
#   title_link: https://api.slack.com/
#   author_link: http://flickr.com/bobby/
#   footer_icon: https://platform.slack-edge.com/img/default_application_icon.png
#   ts: 123456789
#   color: a64f36
#   fields:
#   - title: 'Priority'
#     value: 'High'
#     short: false
#   fallback: 'Required plain-text summary of the attachment.'
#
#
#
#
# ---------------------------------------------- Emoji List ----
# :dpa_antwort:	https://emoji.slack-edge.com/T09LQNVSP/dpa_antwort/7af9007ea9bb818d.png
# :dpa_material:	https://emoji.slack-edge.com/T09LQNVSP/dpa_material/8c884ce656928adf.png
# :dpa_tendenz_unsicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_unsicher/bf605b38f539ebde.png
# :dpa_abschluss_verifikation:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation/5ecbcc5c4c8dc36c.png
# :dpa_tendenz_wahr:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_wahr/a20e1c1cdc113bd0.png
# :dpa_angelegenheit_unsicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_unsicher/0f930e11450ba0c2.png
# :dpa_abschluss_verifikation_ungeloest:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_ungeloest/6f3c57539c9e0f39.png
# :dpa_abschluss_verifikation_wahr:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_wahr/aff509a22fa60fd9.png
# :dpa_angelegenheit_erschrocken:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_erschrocken/f548aa2bbf6a49f9.png
# :dpa_update:	https://emoji.slack-edge.com/T09LQNVSP/dpa_update/08ddf1d64fa1673e.png
# :dpa_tendenz:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz/9f82bdd66657e137.png
# :dpa_angelegenheit_besorgt:	https://emoji.slack-edge.com/T09LQNVSP/dpa_angelegenheit_besorgt/209f22f75a899a25.png
# :dpa_tendenz_falsch:	https://emoji.slack-edge.com/T09LQNVSP/dpa_tendenz_falsch/dec6981f42004276.png
# :dpa_abschluss_verifikation_falsch:	https://emoji.slack-edge.com/T09LQNVSP/dpa_abschluss_verifikation_falsch/a892f9de7ec7ba42.png
# :dpa_verantwortlicher:	https://emoji.slack-edge.com/T09LQNVSP/dpa_verantwortlicher/011f90039fc8d933.png
# :dpa_aktivitaet:	https://emoji.slack-edge.com/T09LQNVSP/dpa_aktivitaet/9960ad5d96aa37ef.png
# :dpa_daniel:	https://emoji.slack-edge.com/T09LQNVSP/dpa_daniel/d26738e945c4215b.jpg
# :dpa_froben:	https://emoji.slack-edge.com/T09LQNVSP/dpa_froben/12cc48dd1bc5c728.jpg
# :dpa_roland:	https://emoji.slack-edge.com/T09LQNVSP/dpa_roland/7fa3bd8d9936e4c1.jpg
# :dpa_stefan:	https://emoji.slack-edge.com/T09LQNVSP/dpa_stefan/c4b0c5b559a854a8.jpg
# :dpa_dots:	https://emoji.slack-edge.com/T09LQNVSP/dpa_dots/8e3f43757035bcf7.png
#

""")



