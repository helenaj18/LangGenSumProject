import glob
import os
import random

# Specify the folder path and file pattern
folder_path = 'Outputs/txt_files'
file_pattern = '*.txt'  # Example: List all .txt files

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))


def create_only_male_dataset(female_names, male_names, files):
    for filename in files:
        with open(filename, "r") as file:
            transcript = file.read()
    
        for name in female_names:
            if name in transcript:
                substitute_name = random.choice(male_names)
                transcript = transcript.replace(name, substitute_name)
        
        new_dataset_filename = filename[:-4].replace("/txt_files/", "/txt_files_male_only/")+'.txt'
        with open(new_dataset_filename, "w") as male_file:
            male_file.write(transcript)

def create_only_female_dataset(female_names, male_names, files):
    for filename in files:
        with open(filename, "r") as file:
            transcript = file.read()
    
        for name in male_names:
            if name in transcript:
                substitute_name = random.choice(female_names)
                transcript = transcript.replace(name, substitute_name)
        
        new_dataset_filename = filename[:-4].replace("/txt_files/", "/txt_files_female_only/")+'.txt'
        with open(new_dataset_filename, "w") as male_file:
            male_file.write(transcript)


def create_neutral_dataset(female_names, male_names, files):
    for filename in files:
        with open(filename, "r") as file:
            transcript = file.read()
    
        for name in male_names:
            if name in transcript:
                substitute_name = 'FIRST_NAME'
                transcript = transcript.replace(name, substitute_name)
        
        for name in female_names:
            if name in transcript:
                substitute_name = 'FIRST_NAME'
                transcript = transcript.replace(name, substitute_name)
        
        new_dataset_filename = filename[:-4].replace("/txt_files/", "/txt_files_no_gender/")+'.txt'
        with open(new_dataset_filename, "w") as male_file:
            male_file.write(transcript)


female_names = ["Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan",\
                "Jessica", "Sarah", "Karen", "Lisa", "Nancy", "Betty", "Sandra", "Margaret",\
                    "Ashley", "Kimberly", "Emily", "Donna", "Michelle", "Carol", "Amanda",\
                        "Melissa", "Deborah", "Stephanie", "Dorothy", "Rebecca", "Sharon",\
                            "Laura", "Cynthia", "Amy", "Kathleen", "Angela", "Shirley",\
                                "Branda", "Emma", "Anna", "Pamela", "Nicole", "Samantha",\
                                    "Katherine", "Christine", "Helen", "Debra", "Rachel",\
                                        "Carolyn", "Janet", "Maria", "Catherine", "Heather",\
                                            "Diane", "Olivia", "Julie", "Joyce", "Victoria",\
                                                "Ruth", "Virginia", "Lauren", "Kelly", "Christina",\
                                                    "Joan", "Evelyn", "Judith", "Andrea", "Hannah",\
                                                        "Megan", "Cheryl", "Jacqueline", "Marhta", "Madison",\
                                                            "Teresa", "Gloria", "Sara", "Janice", "Ann", "Kathryn", \
                                                                "Abigail", "Sophia", "Frances", "Jean", "Alice", "Judy",\
                                                                    "Isabella", "Julia", "Grace", "Amber", "Denise", "Danielle", \
                                                                        "Marilyn", "Beverly", "Charlotte", "Natalie", "Theresa",\
                                                                            "Diana", "Brittany", "Doris", "Kayla", "Alexis", "Lori", "Marie"]



male_names = ["James", "Robert", "John", "Michael", "David", "William", "Richard", "Joseph", "Thomas", "Christopher", "Charles", "Daniel",\
                "Matthew", "Anthony", "Mark", "Donald", "Steven", "Andrew", "Paul", "Joshua", "Kenneth", "Kevin", "Brian", "George", "Timothy",\
                    "Ronald", "Jason", "Edward", "Jeffrey", "Ryan", "Jacob", "Gary", "Nicholas", "Eric", "Jonathan", "Stephen", "Larry",\
                        "Justin", "Scott", "Brandon", "Benjamin", "Samuel", "Gregory", "Alexander", "Patrick", "Frank", "Raymond", "Jack",\
                            "Dennis", "Jerry", "Tyler", "Aaron", "Jose", "Adam", "Nathan", "Henry", "Zachary", "Douglas", "Peter", "Kyle",\
                                "Noah", "Ethan", "Jeremy", "Walter", "Christian", "Keith", "Roger", "Terry", "Austin", "Sean", "Gerald",\
                                    "Carl", "Harold", "Dylan", "Arthur", "Lawrence", "Jordan", "Jesse", "Bryan", "Billy", "Bruce", "Gabriel", "Joe", "Logan", "Alan", \
                                    "Juan", "Albert", "Willie", "Elijah", "Wayne", "Randy", "Vincent", "Mason", "Roy", "Ralph", "Bobby", "Russell", "Bradley", "Philip", "Eugene"]



# create_only_male_dataset(female_names, male_names, files)

# create_only_female_dataset(female_names, male_names, files)

create_neutral_dataset(female_names, male_names, files)