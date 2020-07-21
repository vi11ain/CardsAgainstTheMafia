import pdfkit
import csv
from yattag import Doc
from functools import partial

NOWRAPFORME = ',.?!'
WBRNOTFORME = ' םןךאבגדהוזחטיכלמנסעפצקרשתץף'


def load_cards(filename, dest):
    with open(filename, encoding='utf-8-sig') as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 1:
                row = list(filter(None, row))
            if len(row) == 1:
                dest.append(row[0])
            elif len(row) == 0:
                continue
            else:
                raise ValueError("PROBLEM ENCOUNTERED!")


def generate_back(doc, isQuestions):
    black = " black" if isQuestions else ""

    with doc.tag('div', klass="card title"+black):
        doc.text("קלפים")
        doc.stag('br')
        doc.text("נגד")
        doc.stag('br')
        doc.text("המאפיה")


def generate_front_answers(doc, answers):
    for answer in answers:
        with doc.tag('div', klass='card'):
            doc.text(answer)
            doc.asis('<img src="default.png"/>')


def calcSize(i, question):
    area = question[:i]
    area = area.replace('\n', '')
    length = len(area) % 19
    if length >= 15:
        return 20
    elif length >= 10:
        return 50
    elif length >= 6:
        return 75
    return 100


def generate_front_questions(doc, questions):
    close_span_flag = False
    for question in questions:
        with doc.tag('div', klass='card black'):
            for i in range(len(question)):
                if(close_span_flag):
                    doc.asis(f'{question[i]}</span>')
                    close_span_flag = False
                else:
                    if question[i] == '_':
                        if i == len(question)-1 or question[i+1] not in NOWRAPFORME:
                            doc.asis(
                                f'<span class="placeholder" style="width: {calcSize(i,question)}px;"></span>')
                        else:
                            with doc.tag('span', klass='nowrap'):
                                doc.asis(
                                    f'<span class="placeholder" style="width: {calcSize(i,question)}px;">')
                                close_span_flag = True
                    elif question[i] == '\n':
                        doc.asis('<br>')
                    else:
                        if i != len(question)-1:
                            if question[i] not in WBRNOTFORME and question[i+1] == '_':
                                doc.asis('<wbr>')
                                doc.asis(question[i])
                                continue
                        doc.asis(question[i])
            doc.asis('<img src="defaultblack.png"/>')


def main():

    questions, answers = [], []

    load_cards('a.csv', answers)
    load_cards('q.csv', questions)

    tasks = {
        "answers-back": partial(generate_back, isQuestions=False),
        "answers-front": partial(generate_front_answers, answers=answers),
        "questions-back": partial(generate_back, isQuestions=True),
        "questions-front": partial(generate_front_questions, questions=questions)
    }

    for key in tasks:
        doc = Doc()
        doc.asis('<!DOCTYPE html>')
        with doc.tag('html'):
            with doc.tag('head'):
                doc.asis('<link rel="stylesheet" href="style.css"/>')
            with doc.tag('body'):
                tasks[key](doc=doc)
        with open('design/index.html', 'w+', encoding='utf-8') as f:
            f.write(doc.getvalue())

        pdfkit.from_file('design\\index.html', f'{key}.pdf', options={'--zoom': 1.24, '--margin-bottom': '0', '--margin-top': '0', '--margin-left': '0',
                                                                      '--margin-right': '0', '--enable-local-file-access': None, '--page-width': '60mm', '--page-height': '90mm', '--encoding': 'utf-8'})


if __name__ == "__main__":
    main()
