class Quiz:

    def __init__(self, name, topic, difficulty, questions):
        self.name = name
        self.topic = topic
        self.difficulty = difficulty
        self.quetions = questions


    @staticmethod
    def quiz_generator():
        name = input('What is the name of this quiz? ')
        topic = input('What is this quiz about? ')
        difficulty = input('On a scale of 0 to 3, how hard is this quiz? ')
        questions = []
        while True:
            question = Question.question_input()
            if question ==  'stop':
                break
            questions.append(question)
            answers = Question.answer_input()
            questions.append(answers)
        return name, topic, difficulty, questions


class Question:

    def __init__(self, question_text, answer_dict):
        self.question_text = question_text
        self.answer_dict = answer_dict

    @staticmethod
    def answer_input():
        answer_dict = {}
        while True:
            answer = input('Enter an answer to the question, if you want to stop, enter \'stop\': ')
            if answer.lower() == 'stop':
                break
            iscorrect = input('Is the answer correct?  Enter True or False: ')
            answer_dict[answer] = iscorrect
        return answer_dict

    @staticmethod
    def question_input():
        question_text = input('Enter a question, to stop entering questions enter \'stop\': ' )
        return question_text

q1 = Quiz.quiz_generator()
print(q1)
#TODO add input checker for answer_dict, to verify that the answers entered are True or False, see boolean_helper from Churn
#TODO add input check for difficulty variable to verify that is an integer inclusively between 0 and 3.
