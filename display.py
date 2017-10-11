from models import *
from distutils.util import strtobool
from pathlib import Path
from Quiz_Input3 import TAG
from renderers import *
import os
import json


def quiz_object_builder(quiz_json):
    if 'tag' in quiz_json:
        tag = quiz_json['tag']
    else:
        tag = None
    name = quiz_json['name']
    topic = quiz_json['topic']
    difficulty = quiz_json['difficulty']
    if 'total_points' in quiz_json:
        total_points = quiz_json['total_points']
    else:
        total_points = None
    questions = []
    for q in quiz_json['questions']:
        questions.append(question_object_extractor(q))
    return Quiz(tag, name, topic, difficulty, total_points, questions)

def question_object_extractor(question):
    question_text = question['question_text']
    answer_dict = question['answer_dict']
    points = question['points']
    return(Question(question_text, answer_dict, points))

def quiz_lister(twd_path):
    return [x for x in twd_path.iterdir() if x.name.endswith('.json')]


def quiz_mode_selector():
    #twd = Target Working Directory
    twd_path = Path('.')
    tag = TAG
    commit_list =[]
    json_list = quiz_lister(twd_path)
    print(json_list)
    for i in json_list:
        with open(i, 'r') as fp:
            loader = json.load(fp)
            embedded_tag = quiz_object_builder(loader)
        if embedded_tag.tag == tag:
            commit_list.append(embedded_tag.name)
    print(f'Commit #26 Json List: {commit_list}')
    quiz_name = input('What is the file name for the quiz you would like to take: ')
    if not quiz_name.endswith('.json') :
        quiz_name = quiz_name + '.json'
    else:
        quiz_name = quiz_name
    quiz_types = ('basic', 'b', 'electronic', 'e', 'html', 'h')
    with open(quiz_name, 'r') as fp:
        quiz_json = json.load(fp)
        quiz = quiz_object_builder(quiz_json)
    while True:
        quiz_mode = input(
'''
What type of quiz would you like?  
Enter \'Basic'\ to display a basic, non-interactive quiz.
Enter \'Electronic\' to display an interactive quiz which will be graded electronically. 
Enter \'HTML\' to view the quiz in your browser. 
Quiz Mode: ''')
        quiz_mode = quiz_mode.lower()
        if quiz_mode in ('html', 'h', 'basic', 'b'):
            while True:
                is_clean = input('Do you want to display the rubric?  Enter \'yes\' or \'no\': ')
                try:
                    is_clean = bool(strtobool(is_clean.lower()))
                    break
                except ValueError:
                    print('Enter y, yes, t, true, on, 1, n, no, f, false, off, 0.')
        if quiz_mode in quiz_types:
            break
        print('Please select a valid display option.')
    grade_type = None
    if quiz_mode in ('electronic', 'e'):
        while True:
            grade_type = input('Do you want partial credit multiple-multiple choice, or all or nothing multiple-multiple choice?  Enter \'partial\' or \'all\': ')
            grade_type = grade_type.lower()
            if grade_type in ('all', 'a', 'partial', 'p'):
                break
    display_method = None
    if quiz_mode in ('basic', 'b'):
        display_method = render_to_page(quiz, is_clean)
    if quiz_mode in ('html', 'h'):
        instance = HTMLQuizRender()
        display_method = instance.render(quiz, is_clean)
        save_to_html(f'{quiz_name}.html', display_method)
        os.startfile(f'{quiz_name}.html')
    if quiz_mode in ('electronic', 'e'):
        display_method = quiz_score(electronic_quiz(quiz), grade_type)
    return display_method


def render_to_page(quiz_object, is_clean):
    page = ''
    page += f'Quiz Name: {quiz_object.name}\n'
    page += f'Topic: {quiz_object.topic}\n'
    page += f'Difficulty: {quiz_object.difficulty}\n'
    page += f'Total Points: {quiz_object.total_points}'
    for i in quiz_object.questions:
        iter_count = 1
        page += f'\nQuestion {iter_count}: {i.question_text}\n'
        a_count = 0
        for answer_text, is_true in i.answer_dict.items():
            a_count += 1
            page += f'  Answer {a_count}: [ ] --- {answer_text}\n'
            if is_clean:
                page += f'        Is Answer{a_count} correct?: {is_true}\n'
        iter_count += 1
    return page

def save_to_html(filename, html):
    with open(filename, 'w') as fp:
        fp.write(html)

def electronic_quiz(quiz_object):
    page = ''
    page += f'Quiz Name: {quiz_object.name}\n'
    page += f'Topic: {quiz_object.topic}\n'
    page += f'Difficulty: {quiz_object.difficulty}\n'
    page += f'Total Points: {quiz_object.total_points}'
    master_input_list = []
    master_iscorrect_list = []
    score_list = []
    score_list.append(quiz_object.total_points)
    print(page)
    iter_count = 1
    for q in quiz_object.questions:
        if q.points:
            q_points = q.points
        else:
            q_points = q.total_points/len(quiz_object.questions)
        score_list.append(q_points)
        print(f'\nQuestion {iter_count}: {q.question_text} --- {q_points}pts\n')
        a_count = 0
        input_list = []
        is_correct_list = []
        for answer_text, is_true in q.answer_dict.items():
            a_count += 1
            print(f'  Answer {a_count}: {answer_text}')
            while True:
                iscorrect = input('     Is this answer correct?  Enter True or False: ')
                try:
                    iscorrect = bool(strtobool(iscorrect.lower()))
                    break
                except ValueError:
                    print('Enter y, yes, t, true, on, 1, n, no, f, false, off, 0.')
            input_list.append(iscorrect)
            is_correct_list.append(is_true)
        master_input_list.append(input_list)
        master_iscorrect_list.append(is_correct_list)
    ans_tuple = (master_input_list, master_iscorrect_list, score_list)
    return ans_tuple

def quiz_score(ans_tuple, grade_type):
    actual_score = 0
    input_list = ans_tuple[0]
    iscorrect_list = ans_tuple[1]
    total_points = ans_tuple[2][0]
    for i in range(len(input_list)):
        q_points = ans_tuple[2][i + 1]
        q_score = 0
        for j in range(len(input_list[i])):
            if input_list[i][j] == iscorrect_list[i][j]:
                q_score += q_points / len(input_list[i])
                actual_score += q_points/len(input_list[i])
        if grade_type in ('a', 'all') and input_list[i] != iscorrect_list[i]:
            actual_score -= q_score
    score = (f'Actual: {actual_score}', f'Possible: {total_points}', f'Score: {actual_score}/{total_points} = {(actual_score/total_points)*100}%')
    print(f'Input List: {input_list}')
    print(f'Is_Correct List: {iscorrect_list}')
    return score

quiz = quiz_mode_selector()
print(quiz)



#Mark III Revisions:
    #For quizzes with differentially weighted questions, modify the render_to_page and electronic_quiz methods to display how many points each question is worth.


