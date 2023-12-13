import glob
import os
import random

# Specify the folder path and file pattern
folder_path = 'Outputs/txt_files'
file_pattern = '*.txt'   

# Use glob to get a list of files that match the pattern
files = glob.glob(os.path.join(folder_path, file_pattern))


def create_only_male_dataset(female_names, male_names, files,counter, pronouns_they, pronouns_their, pronouns_them):
    file_counter = 0
    for filename in files:
        summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_legal_led/")+'.txt'
        if os.path.exists(summary_file_name):
            if file_counter < 20:
                with open(filename, "r") as file:
                    transcript = file.read()
            
                for name in female_names:
                    if name in transcript:
                        substitute_name = random.choice(male_names)
                        transcript = transcript.replace(name, substitute_name)
                
                for p in pronouns_they:
                    if p in transcript:
                        transcript = transcript.replace(p, 'they')
                
                for p in pronouns_their:
                    if p in transcript:
                        transcript = transcript.replace(p, 'their')

                for p in pronouns_them:
                    if p in transcript:
                        transcript = transcript.replace(p, 'them')
                
                new_dataset_filename = filename[:-4].replace("/txt_files/", "/gendered/male_only" + str(counter) + "/")+'.txt'
                new_dir = new_dataset_filename.split("A")[0]
                # Check whether the specified path exists or not
                if not os.path.exists(new_dir):
                    # Create a new directory because it does not exist
                    os.makedirs(new_dir)

                with open(new_dataset_filename, "w") as male_file:
                    male_file.write(transcript)
                file_counter += 1
            else:
                break

def create_only_female_dataset(female_names, male_names, files, counter, pronouns_they, pronouns_their, pronouns_them):
    file_counter = 0
    for filename in files:
        summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_legal_led/")+'.txt'
        if os.path.exists(summary_file_name):
            if file_counter < 20:
                with open(filename, "r") as file:
                    transcript = file.read()
            
                for name in male_names:
                    if name in transcript:
                        substitute_name = random.choice(female_names)
                        transcript = transcript.replace(name, substitute_name)
                
                for p in pronouns_they:
                    if p in transcript:
                        transcript = transcript.replace(p, 'they')
                
                for p in pronouns_their:
                    if p in transcript:
                        transcript = transcript.replace(p, 'their')

                for p in pronouns_them:
                    if p in transcript:
                        transcript = transcript.replace(p, 'them')
                
                new_dataset_filename = filename[:-4].replace("/txt_files/", "/gendered/female_only" + str(counter) + "/")+'.txt'
                new_dir = new_dataset_filename.split("A")[0]
                # Check whether the specified path exists or not
                if not os.path.exists(new_dir):
                    # Create a new directory because it does not exist
                    os.makedirs(new_dir)
                with open(new_dataset_filename, "w") as male_file:
                    male_file.write(transcript)
                file_counter += 1
            else:
                break
                


def create_neutral_dataset(female_names, male_names, files, counter, pronouns_they, pronouns_their, pronouns_them):
    for filename in files:
        summary_file_name = filename[:-4].replace("/txt_files/", "/summaries_legal_led/")+'.txt'
        if os.path.exists(summary_file_name):
            if counter < 20:
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
                
                for p in pronouns_they:
                    if p in transcript:
                        transcript = transcript.replace(p, 'they')
                
                for p in pronouns_their:
                    if p in transcript:
                        transcript = transcript.replace(p, 'their')

                for p in pronouns_them:
                    if p in transcript:
                        transcript = transcript.replace(p, 'them')
                
                new_dataset_filename = filename[:-4].replace("/txt_files/", "/gendered/no_gender" + str(counter) + "/")+'.txt'
                new_dir = new_dataset_filename.split("A")[0]
                # Check whether the specified path exists or not
                if not os.path.exists(new_dir):
                    # Create a new directory because it does not exist
                    os.makedirs(new_dir)
                with open(new_dataset_filename, "w") as male_file:
                    male_file.write(transcript)
            else:
                break


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

pronouns_they = [" she ", " he "]
pronouns_their = [" hers ", " his "]
pronouns_them = [" him ", " her "]

for i in range(10):
    create_only_male_dataset(female_names, male_names, files, i, pronouns_they, pronouns_their, pronouns_them)
    create_only_female_dataset(female_names, male_names, files, i, pronouns_they, pronouns_their, pronouns_them)

