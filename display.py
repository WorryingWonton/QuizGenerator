from models import *
import json

def quiz_object_builder(quiz_json):
    name = quiz_json['name']
    topic = quiz_json['topic']
    difficulty = quiz_json['difficulty']
    questions = quiz_json['questions']
    return Quiz(name, topic, difficulty, questions)

def question_object_extractor(quiz_object, index):
    question_text = quiz_object.questions[index]['question_text']
    answer_dict = quiz_object.questions[index]['answer_dict']
    return(Question(question_text, answer_dict))

def quiz_mode_selector():
    quiz_name = input('What is the file name for the quiz you would like to take: ')
    if quiz_name.endswith('.json') != True:
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
    display_method = None
    if quiz_mode == 'clean' or quiz_mode == 'c':
        display_method = render_to_page_clean(quiz)
    if quiz_mode == 'rubric' or quiz_mode == 'r':
        display_method = render_to_page_rubric(quiz)
    if quiz_mode == 'electronic' or quiz_mode == 'e':
        display_method = quiz_score(electronic_quiz(quiz))
    return display_method


def render_to_page_rubric(quiz_object):
    page = ''
    page += f'Quiz Name: {quiz_object.name}\n'
    page += f'Topic: {quiz_object.topic}\n'
    page += f'Difficulty: {quiz_object.difficulty}'
    for i in range(len(quiz_object.questions)):
        q_object = question_object_extractor(quiz_object, i)
        page += f'\nQuestion {i+1}: {q_object.question_text}\n'
        a_count = 0
        for answer_text, is_true in q_object.answer_dict.items():
            a_count += 1
            page += f'  Answer {a_count}: [ ] --- {answer_text}\n'
            page += f'        Is Answer{a_count} correct?: {is_true}\n'
    return page

def render_to_page_clean(quiz_object):
    page = ''
    page += f'Quiz Name: {quiz_object.name}\n'
    page += f'Topic: {quiz_object.topic}\n'
    page += f'Difficulty: {quiz_object.difficulty}'
    for i in range(len(quiz_object.questions)):
        q_object = question_object_extractor(quiz_object, i)
        page += f'\nQuestion {i+1}: {q_object.question_text}\n'
        a_count = 0
        for answer_text in q_object.answer_dict.items():
            a_count += 1
            page += f'  Answer {a_count}: [ ] --- {answer_text[0]}\n'
    return page

def electronic_quiz(quiz_object):
    page = ''
    page += f'Quiz Name: {quiz_object.name}\n'
    page += f'Topic: {quiz_object.topic}\n'
    page += f'Difficulty: {quiz_object.difficulty}'
    master_input_list = []
    master_iscorrect_list = []
    tf_tuple = ('true', 'false')
    print(page)
    for i in range(len(quiz_object.questions)):
        q_object = question_object_extractor(quiz_object, i)
        print(f'\nQuestion {i+1}: {q_object.question_text}\n')
        a_count = 0
        input_list = []
        is_correct_list = []
        for answer_text, is_true in q_object.answer_dict.items():
            a_count += 1
            print(f'  Answer {a_count}: {answer_text}')
            while True:
                iscorrect = input('     Is this answer correct?  Enter True or False: ')
                iscorrect = iscorrect.lower()
                if iscorrect in tf_tuple:
                    break
            input_list.append(iscorrect)
            is_correct_list.append(is_true)
        master_input_list.append(input_list)
        master_iscorrect_list.append(is_correct_list)
    ans_tuple = (master_input_list, master_iscorrect_list)
    return ans_tuple

def quiz_score(ans_tuple):
    possible_score = 0
    actual_score = 0
    input_list = ans_tuple[0]
    iscorrect_list = ans_tuple[1]
    for i in iscorrect_list:
        for j in i:
            possible_score += 1
    for i in range(len(input_list)):
        for j in range(len(input_list[i])):
            if input_list[i][j] == iscorrect_list[i][j]:
                actual_score += 1
    score = (f'Actual: {actual_score}', f'Possible: {possible_score}', f'Score: {actual_score}/{possible_score} = {(actual_score/possible_score)*100}')

    return score

a = quiz_mode_selector()
print(a)



