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
        v1 = self.basic_html(quiz.name, quiz.questions)
        return v1



