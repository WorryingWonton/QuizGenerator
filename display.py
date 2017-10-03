from models import *
from distutils.util import strtobool
import json

def quiz_object_builder(quiz_json):
    name = quiz_json['name']
    topic = quiz_json['topic']
    difficulty = quiz_json['difficulty']
    total_points = quiz_json['total_points']
    questions = quiz_json['questions']
    return Quiz(name, topic, difficulty, total_points, questions)

def question_object_extractor(quiz_object, index):
    question_text = quiz_object.questions[index]['question_text']
    answer_dict = quiz_object.questions[index]['answer_dict']
    points = quiz_object.questions[index]['points']
    return(Question(question_text, answer_dict, points))

def quiz_mode_selector():
    quiz_name = input('What is the file name for the quiz you would like to take: ')
    if not quiz_name.endswith('.json') :
        quiz_name = quiz_name + '.json'
    else:
        quiz_name = quiz_name
    quiz_types = ('clean', 'c', 'rubric', 'r', 'electronic', 'e')
    with open(quiz_name, 'r') as fp:
        quiz_json = json.load(fp)
        quiz = quiz_object_builder(quiz_json)
    while True:
        quiz_mode = input('What type of quiz would you like?  \nEnter \'Clean\' to display a printable quiz without the correct answers shown. \nEnter \'Rubric\' to display a printable quiz with the correct answers shown. \nEnter \'Electronic\' to display an interactive quiz which will be graded electronically. \nQuiz Mode: ' )
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
    if quiz_mode == 'clean' or quiz_mode == 'c':
        is_clean = True
        display_method = render_to_page(quiz, is_clean)
    if quiz_mode == 'rubric' or quiz_mode == 'r':
        is_clean = False
        display_method = render_to_page(quiz, is_clean)
    if quiz_mode == 'electronic' or quiz_mode == 'e':
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


def electronic_quiz(quiz_object):
    page = ''
    page += f'Quiz Name: {quiz_object.name}\n'
    page += f'Topic: {quiz_object.topic}\n'
    page += f'Difficulty: {quiz_object.difficulty}'
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
                actual_score += q_points/len(input_list[i])
                q_score += q_points/len(input_list[i])
        if grade_type in ('a', 'all') and input_list[i] != iscorrect_list[i]:
            actual_score -= q_score
    score = (f'Actual: {actual_score}', f'Possible: {total_points}', f'Score: {actual_score}/{total_points} = {(actual_score/total_points)*100}')
    print(input_list)
    print(iscorrect_list)
    return score

quiz = quiz_mode_selector()
print(quiz)



#MKII Revisions for display:
    #For quizzes with weighted and unweighted questions:
        #Add two multiple-multiple choice question grading modes to quiz_score():
            #The first mode is an all or nothing mode, the true false values in the is_correct list must exactly match the true-false values in the input_list for the question to be considered correct.
            #The second mode (partially implemented already) checks the answers to each question individually and increases actual_score by 1/num_answers*(points or total_points if unweighted) for each match between the is_correct list and the input_list.
            #Add to quiz_mode_selector the ability to display the json files in the present working directory.
                #For MKIII add custom metadata tag in quiz_input module for quiz json files.
