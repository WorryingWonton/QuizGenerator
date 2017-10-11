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

    def render(self,quiz, is_rubric_html):
        body = ''
        body += f'<h1>Quiz Name: {quiz.name}</h1><br/>'
        body += f'<h2>Topic: {quiz.topic}</h2><br/>'
        body += f'Difficulty: {quiz.difficulty}<br/>'
        body += f'Total Points: {quiz.total_points}<br/>'
        body += '<hr/><br/>'
        iter_count = 1
        for i in quiz.questions:
            body += f'<h2>Question {iter_count}: {i.question_text}</h2><br/>'
            a_count = 0
            for answer_text, is_true in i.answer_dict.items():
                a_count += 1
                if is_rubric_html and is_true:
                    body += f'  Answer {a_count}: {answer_text} --- <input type="checkbox" checked="checked"><br/>'
                else:
                    body += f'  Answer {a_count}: {answer_text} --- <input type="checkbox"><br/>'
            iter_count += 1
        return self.basic_html(quiz.name, body)


