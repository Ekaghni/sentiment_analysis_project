from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
import csv
import os
import nltk
nltk.download('vader_lexicon')

def getSentimentValue(selected_csv_file):
    
    try:
        path = "C://Users//ekagh//OneDrive//Desktop//sentiment_api//Ekagni_AI_ML//sentimentAnalysisApi//Sentiment_Project//csv_files//"+selected_csv_file
        with open(path, mode='r') as file:
            reader = csv.DictReader(file)
            column_name = "comments"
            if column_name not in reader.fieldnames:
                print(f"Column '{column_name}' not found in the CSV file.")
                return
            column_data = [row[column_name] for row in reader]
    except Exception as e:
        print(f"Error: {e}")
        
    print(column_data)
    sum = 0
    for x in column_data:

        sia = SentimentIntensityAnalyzer()
        print(sia.polarity_scores(x))
        res = sia.polarity_scores(x)
        if 'compound' in res:
            res = res['compound']
            sum += res
            print(res)
    sentiment_value = sum/len(column_data)
    print('The polarity score of the ',selected_csv_file,' is ',sentiment_value)
    return sentiment_value


def createNewBrand(brand_name):
    directory_path = "C://Users//ekagh//OneDrive//Desktop//sentiment_api//Ekagni_AI_ML//sentimentAnalysisApi//Sentiment_Project//csv_files"
    brand_name = brand_name + ".csv"
    csv_file_path = os.path.join(directory_path, brand_name)
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "comments"])
        writer.writeheader()
    
    print(f"Empty CSV file '{csv_file_path}' created successfully.")


def add_data_to_csv(selected_csv_file, id_value, comments_value):
    fieldnames = ["id", "comments"]
    data = {"id": id_value, "comments": comments_value}
    print("Goinggggggggggg innnnnn add data")
    try:
        path = "C://Users//ekagh//OneDrive//Desktop//sentiment_api//Ekagni_AI_ML//sentimentAnalysisApi//Sentiment_Project//csv_files//"+selected_csv_file
        with open(path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            if file.tell() == 0:
                writer.writeheader()
            writer.writerow(data)

        print(f"Data added to '{selected_csv_file}' successfully.")
    except Exception as e:
        print(f"Error: {e}")    

def menu_nltk():
    print('Manual For Using Sentiment Analysis System-')
    print('1. Create a new brand')
    print('2. Add comments to the existing brands')
    print('3. Run sentiment analysis on brands')
    inp = int(input('Enter the index: '))
    if inp==1:
        createNewBrand()
    elif inp==2:
        add_data_to_csv()
    else:
        print("Nothing selected")
        # driverCode()

# menu_nltk()

