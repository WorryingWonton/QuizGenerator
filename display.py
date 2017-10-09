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
    questions = quiz_json['questions']
    return Quiz(tag, name, topic, difficulty, total_points, questions)

def question_object_extractor(quiz_object, index):
    question_text = quiz_object.questions[index]['question_text']
    answer_dict = quiz_object.questions[index]['answer_dict']
    points = quiz_object.questions[index]['points']
    return(Question(question_text, answer_dict, points))

def quiz_lister(twd_path):
    return [x for x in twd_path.iterdir() if x.name.endswith('.json')]


def quiz_mode_selector():
    #twd = Target Working Directory
    twd_path = Path('.')
    tag = TAG
    commit21_list =[]
    json_list = quiz_lister(twd_path)
    print(json_list)
    for i in json_list:
        with open(i, 'r') as fp:
            loader = json.load(fp)
            embedded_tag = quiz_object_builder(loader)
        if embedded_tag.tag == tag:
            commit21_list.append(embedded_tag.name)
    print(f'Commit #21 Json List: {commit21_list}')
    quiz_name = input('What is the file name for the quiz you would like to take: ')
    if not quiz_name.endswith('.json') :
        quiz_name = quiz_name + '.json'
    else:
        quiz_name = quiz_name
    quiz_types = ('clean', 'c', 'rubric', 'r', 'electronic', 'e', 'html', 'h')
    with open(quiz_name, 'r') as fp:
        quiz_json = json.load(fp)
        quiz = quiz_object_builder(quiz_json)
    while True:
        quiz_mode = input('What type of quiz would you like?  \nEnter \'Clean\' to display a printable quiz without the correct answers shown. \nEnter \'Rubric\' to display a printable quiz with the correct answers shown. \nEnter \'Electronic\' to display an interactive quiz which will be graded electronically. \nEnter \'HTML\' to view the quiz in your browser. \nQuiz Mode: ' )
        quiz_mode = quiz_mode.lower()
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
    if quiz_mode in ('clean', 'c'):
        is_clean = True
        display_method = render_to_page(quiz, is_clean)
    if quiz_mode in ('rubric', 'r'):
        is_clean = False
        display_method = render_to_page(quiz, is_clean)
    if quiz_mode in ('html', 'h'):
        instance = HTMLQuizRender()
        display_method = instance.render(quiz)
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
    for i in range(len(quiz_object.questions)):
        q_object = question_object_extractor(quiz_object, i)
        page += f'\nQuestion {i+1}: {q_object.question_text}\n'
        a_count = 0
        for answer_text, is_true in q_object.answer_dict.items():
            a_count += 1
            page += f'  Answer {a_count}: [ ] --- {answer_text}\n'
            if not is_clean:
                page += f'        Is Answer{a_count} correct?: {is_true}\n'
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
    for i in range(len(quiz_object.questions)):
        q_object = question_object_extractor(quiz_object, i)
        if q_object.points:
            q_points = q_object.points
        else:
            q_points = quiz_object.total_points/len(quiz_object.questions)
        score_list.append(q_points)
        print(f'\nQuestion {i+1}: {q_object.question_text} --- {q_points}pts\n')
        a_count = 0
        input_list = []
        is_correct_list = []
        for answer_text, is_true in q_object.answer_dict.items():
            a_count += 1
            print(f'  Answer {a_count}: {answer_text}')
            while True:
                iscorrect = input('     Is this answer correct?  Enter True or False: ')
                try:
                    iscorrect = strtobool(iscorrect.lower())
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
    #Add html display option for clean and rubric modes.  First implementation will just display a clean quiz.
    #For quizzes with differentially weighted questions, modify the render_to_page and electronic_quiz methods to display how many points each question is worth.


