from nltk.sentiment import SentimentIntensityAnalyzer
from tqdm.notebook import tqdm
import csv
import os
import nltk
import matplotlib.pyplot as plt
import numpy as np
from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification
from scipy.special import softmax
nltk.download('vader_lexicon')
dir ="C://Users//ekagh//OneDrive//Desktop//sentiment_analysis_project//Main_code//"

def driverCode():
    
    csv_files = [file for file in os.listdir(dir) if file.endswith(".csv")]
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
        with open(dir+selected_csv_file, mode='r') as file:
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
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    for x in column_data:

        sia = SentimentIntensityAnalyzer()
        print("Vader Analysis Result for statement-\n ",x,"---->")
        print(sia.polarity_scores(x))
        res = sia.polarity_scores(x)
        if 'compound' in res:
            res = res['compound']
            sum += res
            print(res)

        ##########################

        example = x
        encoded_text = tokenizer(example, return_tensors='pt')
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        scores_dict = {
            'roberta_neg' : scores[0],
            'roberta_neu' : scores[1],
            'roberta_pos' : scores[2]
        }
        print("Roberta Analysis Result for statement-\n ",x,"---->")
        print(scores_dict)

    sentiment_value = sum/len(column_data)
    print('The polarity score using Vader Analysis method of the ',selected_csv_file,' is ',sentiment_value)


def createNewBrand(brand_name):
    brand_name = brand_name+".csv"
    csv_file_name = brand_name
    with open(dir+csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "comments"])
        writer.writeheader()
    print(f"Empty CSV file '{csv_file_name}' created successfully.")


def add_data_to_csv():
    csv_files = [file for file in os.listdir(dir) if file.endswith(".csv")]
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
            with open(dir+selected_csv_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)

            print(f"Data added to '{selected_csv_file}' successfully.")
        except Exception as e:
            print(f"Error: {e}")  

def compare_roberta_vader_sentiments():
    csv_files = [file for file in os.listdir(dir) if file.endswith(".csv")]

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
        with open(dir+selected_csv_file, mode='r') as file:
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
    vader_results = []
    roberta_results = []
    MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
    tokenizer = AutoTokenizer.from_pretrained(MODEL)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL)
    for x in column_data:

        sia = SentimentIntensityAnalyzer()
        # print(sia.polarity_scores(x))
        res = sia.polarity_scores(x)
        vader_results.append(res)

        ##########################

        example = x
        encoded_text = tokenizer(example, return_tensors='pt')
        output = model(**encoded_text)
        scores = output[0][0].detach().numpy()
        scores = softmax(scores)
        scores_dict = {
            'roberta_neg' : scores[0],
            'roberta_neu' : scores[1],
            'roberta_pos' : scores[2]
        }
        roberta_results.append(scores_dict)
    # Extracting sentiments for each model
    vader_neg = [result['neg'] for result in vader_results]
    vader_neu = [result['neu'] for result in vader_results]
    vader_pos = [result['pos'] for result in vader_results]

    roberta_neg = [result['roberta_neg'] for result in roberta_results]
    roberta_neu = [result['roberta_neu'] for result in roberta_results]
    roberta_pos = [result['roberta_pos'] for result in roberta_results]

    # Plotting the results
    fig, axs = plt.subplots(2, 3, figsize=(15, 8))

    # Plotting Vader Sentiments
    axs[0, 0].hist(vader_neg, bins=20, color='red', alpha=0.7, label='Vader Negative')
    axs[0, 1].hist(vader_neu, bins=20, color='green', alpha=0.7, label='Vader Neutral')
    axs[0, 2].hist(vader_pos, bins=20, color='blue', alpha=0.7, label='Vader Positive')

    # Plotting Roberta Sentiments
    axs[1, 0].hist(roberta_neg, bins=20, color='red', alpha=0.7, label='Roberta Negative')
    axs[1, 1].hist(roberta_neu, bins=20, color='green', alpha=0.7, label='Roberta Neutral')
    axs[1, 2].hist(roberta_pos, bins=20, color='blue', alpha=0.7, label='Roberta Positive')

    # Adding labels and legends
    axs[0, 0].set_title('Vader Negative Sentiment')
    axs[0, 1].set_title('Vader Neutral Sentiment')
    axs[0, 2].set_title('Vader Positive Sentiment')

    axs[1, 0].set_title('Roberta Negative Sentiment')
    axs[1, 1].set_title('Roberta Neutral Sentiment')
    axs[1, 2].set_title('Roberta Positive Sentiment')

    for ax in axs.flat:
        ax.set(xlabel='Sentiment Score', ylabel='Frequency')
        ax.legend()

    # Adjusting layout
    plt.tight_layout()
    plt.show()



def menu_nltk():
    print('Manual For Using Sentiment Analysis System-')
    print('1. Create a new brand')
    print('2. Add comments to the existing brands')
    print('3. Run sentiment analysis on brands')
    print('4. Compare Vader vs Roberta model results')
    inp = int(input('Enter the index: '))
    if inp==1:
        brand_name = input("Enter Brand Name: ")
        createNewBrand(brand_name)
    elif inp==2:
        add_data_to_csv()
    elif inp==3:
        driverCode()
    else:
        compare_roberta_vader_sentiments()

menu_nltk()

