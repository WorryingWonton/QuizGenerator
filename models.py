import json
class Quiz:

    def __init__(self, name, topic, difficulty, questions):
        self.name = name
        self.topic = topic
        self.difficulty = difficulty
        self.questions = questions

    @staticmethod
    def from_dict(quiz_dict):
        name = quiz_dict['name']
        topic = quiz_dict['topic']
        difficulty  = quiz_dict['difficulty']
        questions = quiz_dict['questions']
        return Quiz(name, topic, difficulty, questions)

    def __repr__(self):
        return f'Quiz: Name: {self.name}, Topic: {self.topic}, Difficulty: {self.difficulty}, Question & Answer List: {self.questions}'

    def render_to_page(self):
        page = ''
        page += f'Quiz Name: {self.name}\n'
        page += f'Topic: {self.topic}\n'
        page += f'Difficulty: {self.difficulty}\n'
        for i in range(len(self.questions)):
            question_text = self.questions[i]['question_text']
            page += f'Question {i+1}: {question_text}\n'
            a_count = 0
            for answer_text, is_true in self.questions[i]['answer_dict'].items():
                a_count += 1
                page += f'  Answer {a_count}: [] --- {answer_text}\n'
                page += f'        Is Answer{a_count} correct?: {is_true}\n'

        return page



class Question:

    def __init__(self, question_text, answer_dict):
        self.question_text = question_text
        self.answer_dict = answer_dict

    @staticmethod
    def from_dict(question_dict):
        question_text = question_dict['questions']
        qlist = []
        for i in question_dict['questions']:
            qlist.append(Quiz.from_dict(i))
        return(Question(question_text, qlist))


filename = 'Quiz_Input_Test2.json'
with open(filename, 'r') as fp:
    quiz_dict = json.load(fp)
    q = Quiz.from_dict(quiz_dict)
    p = Quiz.render_to_page(q)

print(q)
print(p)
