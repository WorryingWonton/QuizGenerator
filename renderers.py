from models import*
class HTMLQuizRender:
    def basic_html(self, title, body):
        return f'''
        <html>
            <head>
                <title>
                {title}
                </title>
            </head>
            <body>
            {body}
            </body>            
        </html>
        '''

    def render(self,quiz):
        body = ''
        body += f'<h1>Quiz Name: {quiz.name}</h1><br/>'
        body += f'<h2>Topic: {quiz.topic}</h2><br/>'
        body += f'Difficulty: {quiz.difficulty}<br/>'
        body += f'Total Points: {quiz.total_points}<br/>'
        body += '<hr/><br/>'
        for i in range(len(quiz.questions)):
            question = question_object_extractor(quiz, i)
            body += f'<h2>Question {i+1}: {question.question_text}</h2><br/>'
            a_count = 0
            for answer_text, is_true in question.answer_dict.items():
                a_count += 1
                body += f'  Answer {a_count}: {answer_text} --- <input type="checkbox"><br/>'
        return self.basic_html(quiz.name, body)

def question_object_extractor(quiz_object, index):
    question_text = quiz_object.questions[index]['question_text']
    answer_dict = quiz_object.questions[index]['answer_dict']
    points = quiz_object.questions[index]['points']
    return (Question(question_text, answer_dict, points))

