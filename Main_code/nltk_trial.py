from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
import csv
import os
import nltk
nltk.download('vader_lexicon')

def driverCode():
    csv_files = [file for file in os.listdir() if file.endswith(".csv")]
    print("Available CSV files:")
    for index, file in enumerate(csv_files, start=1):
        print(f"{index}. {file}")
    try:
        selected_index = int(input("Enter the index of CSV file on which you want to run the sentiment analysis: "))
        selected_csv_file = csv_files[selected_index - 1]
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number.")
        exit()
    try:
        with open(selected_csv_file, mode='r') as file:
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


def createNewBrand(brand_name):
    brand_name = brand_name+".csv"
    csv_file_name = brand_name
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "comments"])
        writer.writeheader()
    print(f"Empty CSV file '{csv_file_name}' created successfully.")


def add_data_to_csv():
    csv_files = [file for file in os.listdir() if file.endswith(".csv")]
    print("Available CSV files:")
    for index, file in enumerate(csv_files, start=1):
        print(f"{index}. {file}")
    try:
        selected_index = int(input("Enter the number corresponding to the CSV file you want to use: "))
        selected_csv_file = csv_files[selected_index - 1]
    except (ValueError, IndexError):
        print("Invalid input. Please enter a valid number.")
        exit()
    fieldnames = ["id", "comments"]
    number_of_times_data_to_be_added = int(input('Enter The Number of Times You Want To Add The Data: '))
    for i in range(0,number_of_times_data_to_be_added):
        id_value = input("Enter the ID: ")
        comments_value = input("Enter the comments: ")
        data = {"id": id_value, "comments": comments_value}
        try:
            with open(selected_csv_file, mode='a', newline='') as file:
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
        driverCode()

menu_nltk()

