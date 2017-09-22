import json
from models import *


def quiz_meta():
    name = input('What is the name of this quiz? ')
    topic = input('What is this quiz about? ')
    d_scale = ('0','1','2','3')
    while True:
        difficulty = input(f'On a scale of {d_scale[0]} to {d_scale[-1]}, how hard is this quiz? ')
        if difficulty in d_scale:
            break
    metalist = (name, topic, difficulty)
    return metalist

def question_generator():
    question_text = input('Enter a question, when you are done entering questions type \'stop\': ')
    if question_text.lower() == 'stop':
        return None
    answer_dict = {}
    while True:
        answer = input('Enter an answer to the question, when you are done entering answers, type \'stop\': ')
        if answer.lower() == 'stop':
            break
        while True:
            iscorrect = input('Is the above answer correct?  Enter True or False: ')
            if iscorrect.lower() == 'true' or iscorrect.lower() == 'false':
                break
        answer_dict[answer] = iscorrect
    qapair = (question_text, answer_dict)
    return qapair

def question_list_builder():
    questions = []
    while True:
        qg_method = question_generator()
        if qg_method is None:
            break
        q = Question(qg_method[0], qg_method[1])
        questions.append(q)
    return questions




class ObjectEncoder(json.JSONEncoder):
  def default(self, obj):
    return obj.__dict__


qmeta = quiz_meta()
questions = question_list_builder()
quiz = Quiz(qmeta[0], qmeta[1], qmeta[2], questions)
def JSONWrite(quiz, filepath):
    with open(f'{filepath}.json', 'w') as fp:
        fp.write(quiz)
JSONWrite(json.dumps(quiz, cls=ObjectEncoder), qmeta[0])


print(json.dumps(quiz, cls=ObjectEncoder))

