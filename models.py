class Quiz:

    def __init__(self, tag, name, topic, difficulty, total_points, questions):
        self.tag = tag
        self.name = name
        self.topic = topic
        self.difficulty = difficulty
        self.total_points = total_points
        self.questions = questions

class Question:

    def __init__(self, question_text, answer_dict, points):
        self.question_text = question_text
        self.answer_dict = answer_dict
        self.points = points


#MKII Modification outline for models:
    #Quiz class:  Add attribute for total score, genderated by sum of individual scores for question objects in quiz_input.
    #Question class:  Add attribute for individual question worth.  If all questions are equally weighted, set attribute to None in quiz_input.