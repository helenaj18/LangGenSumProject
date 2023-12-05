
import os

folder_path = '/Users/helenajonsdottir/Library/Mobile Documents/com~apple~CloudDocs/Desktop/Columbia/Courses/Language generation and summarization/Code/Outputs/transcripts'

if os.path.exists(folder_path) and os.path.isdir(folder_path):
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    num_files = len(files)
    print(f'The folder {folder_path} contains {num_files} files.')
else:
    print(f'The folder {folder_path} does not exist or is not a directory.')
