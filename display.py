from models import *

def quiz_object_builder(quiz_json):
    name = quiz_json['name']
    topic = quiz_json['topic']
    difficulty = quiz_json['difficulty']
    questions = quiz_json['questions']
    return Quiz(name, topic, difficulty, questions)

def render_to_page(quiz_object):
    page = ''
    page += f'Quiz Name: {quiz_object.name}\n'
    page += f'Topic: {quiz_object.topic}\n'
    page += f'Difficulty: {quiz_object.difficulty}\n'
    for i in range(len(quiz_object.questions)):
        q_object = question_object_extractor(quiz_object, i)
        page += f'Question {i+1}: {q_object.question_text}\n'
        a_count = 0
        for answer_text, is_true in q_object.answer_dict.items():
            a_count += 1
            page += f'  Answer {a_count}: [] --- {answer_text}\n'
            page += f'        Is Answer{a_count} correct?: {is_true}\n'
    return page


def question_object_extractor(quiz_object, iterator):
    question_text = quiz_object.questions[iterator]['question_text']
    answer_dict = quiz_object.questions[iterator]['answer_dict']
    return(Question(question_text, answer_dict))


filename = 'Input and Encoding Test 3.json'
with open(filename, 'r') as fp:
    quiz_json = json.load(fp)
    quiz = quiz_object_builder(quiz_json)
    print(quiz.questions)
    p = render_to_page(quiz)

print(p)





