from models import *
from distutils.util import strtobool
# from models import TAG
import json

#Pre-Commit 26
TAG = 23456

def quiz_meta():
    name = input('What is the name of this quiz? ')
    topic = input('What is this quiz about? ')
    d_scale = ('0','1','2','3')
    tag = TAG
    total_points = None
    while True:
        difficulty = input(f'On a scale of {d_scale[0]} to {d_scale[-1]}, how hard is this quiz? ')
        if difficulty in d_scale:
            break
    while True:
        is_weighted = input ('Will the questions be weighted differently?  Enter \'yes\' if they will be and \'no\' if they won\'t be: ')
        try:
            is_weighted = strtobool(is_weighted.lower())
            break
        except ValueError:
            print('Enter y, yes, t, true, on, 1, n, no, f, false, off, 0.')
    if is_weighted == 0:
        while True:
            total_points = input('Enter a number representing in total how many points this quiz is worth: ')
            try:
                total_points = abs(float(total_points))
                break
            except ValueError:
                print('Please enter a number.')
    metalist = (tag, name, topic, difficulty, total_points)
    return metalist

def question_generator(total_points):
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
            try:
                iscorrect = bool(strtobool(iscorrect.lower()))
                break
            except ValueError:
                print('Enter  y, yes, t, true, on, 1, n, no, f, false, off, 0.')
        answer_dict[answer] = iscorrect
    points = None
    while True:
        if total_points != None:
            break
        points = input('How many points is this question worth? Enter a number: ')
        try:
            points = abs(float(points))
            break
        except ValueError:
            print('Please enter a number.')
    qapair = (question_text, answer_dict, points)
    return qapair

def question_list_builder(total_points):
    questions = []
    while True:
        qg_method = question_generator(total_points)
        if qg_method is None:
            break
        q = Question(qg_method[0], qg_method[1], qg_method[2])
        questions.append(q)
    return questions

def weighted_total_points_finder(questions):
    total_weighted_points = 0
    for i in questions:
        total_weighted_points += i.points
    return total_weighted_points

class ObjectEncoder(json.JSONEncoder):
  def default(self, obj):
    return obj.__dict__

if __name__ == '__main__':
    qmeta = quiz_meta()
    questions = question_list_builder(qmeta[4])
    if qmeta[4] == None:
        quiz_points = weighted_total_points_finder(questions)
        quiz = Quiz(qmeta[0], qmeta[1], qmeta[2], qmeta[3], quiz_points, questions)
    else:
        quiz = Quiz(qmeta[0], qmeta[1], qmeta[2], qmeta[3], qmeta[4], questions)
    def JSONWrite(quiz, filepath):
        with open(f'{filepath}.json', 'w') as fp:
            fp.write(quiz)
    JSONWrite(json.dumps(quiz, cls=ObjectEncoder), qmeta[1])

    print(json.dumps(quiz, cls=ObjectEncoder))
