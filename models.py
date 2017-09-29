class Quiz:

    def __init__(self, name, topic, difficulty, questions):
        self.name = name
        self.topic = topic
        self.difficulty = difficulty
        self.questions = questions


class Question:

    def __init__(self, question_text, answer_dict):
        self.question_text = question_text
        self.answer_dict = answer_dict



