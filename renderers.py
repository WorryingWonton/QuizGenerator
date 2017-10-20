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

    def render(self,quiz, is_clean_html):
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
                body += f'  Answer {a_count}: {answer_text} --- <input type="checkbox"><br/>'
                if is_clean_html:
                    body += f'      Rubric:  {is_true}<br/>'
            iter_count += 1
        return self.basic_html(quiz.name, body)

class TextQuizRenderer:

    def render(self, quiz_object, is_clean):
        page = ''
        page += f'Quiz Name: {quiz_object.name}\n'
        page += f'Topic: {quiz_object.topic}\n'
        page += f'Difficulty: {quiz_object.difficulty}\n'
        page += f'Total Points: {quiz_object.total_points}'
        for i in quiz_object.questions:
            iter_count = 1
            page += f'\nQuestion {iter_count}: {i.question_text}\n'
            a_count = 0
            for answer_text, is_true in i.answer_dict.items():
                a_count += 1
                page += f'  Answer {a_count}: [ ] --- {answer_text}\n'
                if is_clean:
                    page += f'        Is Answer{a_count} correct?: {is_true}\n'
            iter_count += 1
        return page










