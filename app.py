import pdfkit
from yattag import Doc

with open('answers.txt', encoding='utf-8') as f:
    answers = f.readlines()

with open('questions.txt', encoding='utf-8') as f:
    questions = f.readlines()

doc, tag, text = Doc().tagtext()
doc.asis('<!DOCTYPE html>')
with tag('html'):
    with tag('head'):
        doc.asis('<link rel="stylesheet" href="style.css"/>')
    with tag('body'):
        # Answer cards back
        with tag('div', klass='card'):
            with tag('p', klass='card-back-title'):
                text('קלפים נגד המאפיה')
        # Answer cards front
        for answer in answers:
            with tag('div', klass='card'):
                with tag('p'):
                    text(answer)
                doc.asis('<img src="default.png"/>')
        # Question cards back
        with tag('div', klass='card question'):
            with tag('p', klass='card-back-title'):
                text('קלפים נגד המאפיה')
        # Question cards front
        for question in questions:
            with tag('div', klass='card question'):
                with tag('p'):
                    text(question)
                doc.asis('<img src="default.png"/>')

with open('design/index.html', 'w+', encoding='utf-8') as f:
    f.write(doc.getvalue())

pdfkit.from_file('design\\index.html', 'out.pdf', options={'--zoom': 1.261, '--margin-bottom': '0', '--margin-top': '0', '--margin-left': '0',
                                                           '--margin-right': '0', '--enable-local-file-access': None, '--page-width': '60mm', '--page-height': '90mm', '--encoding': 'utf-8'})
