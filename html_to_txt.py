import glob
import os
from bs4 import BeautifulSoup
import re

# Specify the folder path and file pattern
folder_path = 'Outputs/Transcripts'
file_pattern = '*.html'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))

# Iterate over the files
for filename in files:
    with open(filename) as file:
        html_content = file.read()
    
    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # I also used this target class:
    # target_class = "jc_is jc_EZ"
    target_class = "jd_l5 s_et"

    # Find the div with the specified class
    target_div = soup.find('div', class_=re.compile(r'\b' + re.escape(target_class) + r'\b'))

    # Check if the target div is found
    if target_div:
        # Extract the content within the div
        content = target_div.get_text()
        text_file_name = filename[:-5].replace("/Transcripts/", "/txt_files/")+'.txt'
        if not os.path.exists(text_file_name):
            with open(text_file_name, 'w') as text_file:
                text_file.write(content)
    else:
        print("Target div not found in the HTML file:", filename)

