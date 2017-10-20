import argparse, json, os
from display import quiz_object_builder, save_to_html
from renderers import*
from pathlib import Path
from Quiz_Input3 import TAG

parser = argparse.ArgumentParser(description= 'Command Line Quiz Display Utility')
parser.add_argument('filename', nargs = '*', help='Enter the exact filenames for the quizzes you want to open, be sure they are compatible with the renderer methods..')
parser.add_argument('--type', help='Enter clean, c, rubric, or r.')
parser.add_argument('--mode', help='Enter html, h, basic, or b.')
args = parser.parse_args()
args.mode = args.mode.lower()
if args.mode not in ('h', 'html', 'b', 'basic'):
    print(f'{args.mode.upper()} is not valid, please enter h, html, basic, or b.')
else:
    # True = Display Rubric, False = Hide Rubric
    if args.type in ('rubric', 'r'):
        is_clean = True
    else:
        is_clean = False

    if len(args.filename) == 1:
        directory = args.filename[0]
    else:
        directory = None
    if directory:
        b = Path(directory).is_dir()
    else:
        b = False

    def hamburgler_helper(args_mode, quiz_object):
        if args_mode in ('basic', 'b'):
            instance = TextQuizRenderer()
            display_method = instance.render(quiz_object, is_clean)
            print(display_method)
        elif args_mode in ('html', 'h'):
            instance = HTMLQuizRender()
            display_method = instance.render(quiz_object, is_clean)
            save_to_html(f'{i}.html', display_method)
            os.startfile(f'{i}.html')

    def tag_check(file_name):
        with open(file_name, 'r') as fp:
            quiz_json = json.load(fp)
            quiz_object = quiz_object_builder(quiz_json)
        if quiz_object.tag == TAG:
            return quiz_object
        else:
            return None

    if b:
        just_json = [x for x in Path(directory).iterdir() if x.name.endswith('.json')]
        for i in just_json:
            if tag_check(i):
                hamburgler_helper(args.mode, tag_check(i))

    else:
        for i in args.filename:
            with open(i, 'r') as fp:
                quiz_json = json.load(fp)
                quiz_object = quiz_object_builder(quiz_json)
                hamburgler_helper(args.mode, quiz_object)







