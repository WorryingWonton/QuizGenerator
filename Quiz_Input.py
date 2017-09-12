class Quiz:
    def __init__(self, name, topic, questions, difficulty):
        self.name = name
        self.topic = topic
        self.questions = questions
        self.difficulty = difficulty

    def quiz_generator(self):
        pass

# class Question:
#     def __init__(self, question_text, answer_dict):
#         self.question_text = question_text
#         self.answer_dict =

    # def __repr__(self):
    #     return f'Q: {self.question_text}, A: {self.answer_dict}'


class Question:
    def __init__(self, question_dict):
        self.question_dict = question_dict

    def __repr__(self):
        return f'{self.question_dict}'

def question_input():

    question_dict = {}
    while True:
        question = input('Enter a question, to stop entering questions enter \'stop\': ')
        if question.lower() == 'stop':
            break
        answer_dict = {}
        question_dict[question] = answer_dict
        while True:
            answer = input('Enter an answer to the question, enter \'stop\' to quit entering answers: ')
            if answer.lower() == 'stop':
                break
            #TODO Modify iscorrect.lower() to only accept 'true' or 'false' as answers, raise exception if the answer provided is not either of those two things.
            iscorrect = input('Is the answer correct?  Enter True or False: ')
            answer_dict[answer] = iscorrect

    return Question(question_dict)


q1 = question_input()
print(q1)

