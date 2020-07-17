import pdfkit
from yattag import Doc

with open('answers.txt', encoding='utf-8') as f:
    answers = f.readlines()

doc, tag, text = Doc().tagtext()
doc.asis('<!DOCTYPE html>')
with tag('html', style=""):
    with tag('head'):
        doc.asis('<link rel="stylesheet" href="style.css"/>')
    with tag('body'):
        for answer in answers:
            with tag('div', klass='answer-card'):
                with tag('p'):
                    text(answer)
                doc.asis('<img src="default.png"/>')

with open('design/index.html', 'w+', encoding='utf-8') as f:
    f.write(doc.getvalue())

pdfkit.from_file('design\\index.html', 'out.pdf', options={'--margin-bottom': '0mm', '--margin-top': '0mm', '--margin-left': '0mm',
                                                           '--margin-right': '0mm', '--enable-local-file-access': None, '--page-width': '60mm', '--page-height': '90mm', '--encoding': 'utf-8'})
