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
#True = Display Rubric, False = Hide Rubric
if args.type in ('rubric', 'r'):
    is_clean = True
else:
    is_clean = False



#file_list = []
#if args.filename == a_directory:
#   for i in a_directory:
#       if i.tag == current_tag:
#           filelist.append(i.name)

mode = None

#Behavior:  if args.filename is a path object:  for each file in the directory, check if the file has a valid tag.

if len(args.filename) == 1:
    directory = args.filename[0]
else:
    directory = None

if directory:
    b = Path(directory).is_dir()
else:
    b = False

if b:
    just_json = [x for x in Path(directory).iterdir() if x.name.endswith('.json')]
    for i in just_json:
        with open(i, 'r') as fp:
            quiz_json = json.load(fp)
            quiz_object = quiz_object_builder(quiz_json)
            if quiz_object.tag == TAG:
                if args.mode.lower() in ('basic', 'b'):
                    instance = TextQuizRenderer()
                    display_method = instance.render(quiz_object, is_clean)
                    print(display_method)
                elif args.mode.lower() in ('html', 'h'):
                    instance = HTMLQuizRender()
                    display_method = instance.render(quiz_object, is_clean)
                    save_to_html(f'{i}.html', display_method)
                    os.startfile(f'{i}.html')
                else:
                    print(f'{args.mode.upper()} is not valid, please enter h, html, basic, or b.')
                    break
else:
    for i in args.filename:
        with open(i, 'r') as fp:
            quiz_json = json.load(fp)
            quiz_object = quiz_object_builder(quiz_json)
            if args.mode.lower() in ('basic', 'b'):
                instance = TextQuizRenderer()
                display_method = instance.render(quiz_object, is_clean)
                print(display_method)
            elif args.mode.lower() in ('html', 'h'):
                instance = HTMLQuizRender()
                display_method = instance.render(quiz_object, is_clean)
                save_to_html(f'{i}.html', display_method)
                os.startfile(f'{i}.html')
            else:
                print(f'{args.mode.upper()} is not valid, please enter h, html, basic, or b.')
                break






# args: --type (clean or rubric), --mode (basic, html), filename(s) or quiz files in currnt directory

#TODO:  Add functionality to display all quizzes with the correct Tag.