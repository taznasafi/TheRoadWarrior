import os

if not os.path.exists(r".\logs"):
    print("creating logging folder")
    os.makedirs(r".\logs")

if not os.path.exists(r'.\data\input'):
    print("creating input folder")
    os.makedirs('.\data\input')
_input_path = '.\data\input'
if not os.path.exists(r'.\data\output'):
    print("creating output folder")
    os.makedirs('.\data\output')
_output_path = '.\data\output'