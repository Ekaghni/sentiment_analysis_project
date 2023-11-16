import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import ttk, simpledialog
from tkinter import filedialog
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
dir = "C://Users//ekagh//OneDrive//Desktop//sentiment_analysis_project//Main_code//"

class SentimentAnalysisApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sentiment Analysis App")

        self.menu_frame = ttk.Frame(root)
        self.menu_frame.pack(pady=10)

        self.menu_label = ttk.Label(self.menu_frame, text="Select an option:")
        self.menu_label.grid(row=0, column=0, padx=10)

        self.menu_combobox = ttk.Combobox(self.menu_frame, values=["Create New Brand", "Add Comments", "Run Sentiment Analysis", "Compare Vader vs Roberta"])
        self.menu_combobox.grid(row=0, column=1, padx=10)
        self.menu_combobox.set("Select")

        self.run_button = ttk.Button(self.menu_frame, text="Run", command=self.run_selected_option)
        self.run_button.grid(row=0, column=2, padx=10)

    def run_selected_option(self):
        selected_option = self.menu_combobox.get()
        if selected_option == "Create New Brand":
            self.create_new_brand()
        elif selected_option == "Add Comments":
            self.add_comments()
        elif selected_option == "Run Sentiment Analysis":
            self.run_sentiment_analysis()
        elif selected_option == "Compare Vader vs Roberta":
            self.compare_vader_roberta_sentiments()

    def create_new_brand(self):
        brand_name = simpledialog.askstring("Create New Brand", "Enter Brand Name:")
        if brand_name:
            createNewBrand(brand_name)

    def add_comments(self):
        add_data_app = AddDataToCSVApp(tk.Toplevel(self.root))

    def run_sentiment_analysis(self):
        driver_app = DriverCodeApp(tk.Toplevel(self.root))

    def compare_vader_roberta_sentiments(self):
        compare_roberta_vader_sentiments()

class AddDataToCSVApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Data to CSV")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.selected_csv_file = tk.StringVar()

        self.csv_file_label = ttk.Label(self.frame, text="Select CSV file:")
        self.csv_file_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

        self.csv_file_combobox = ttk.Combobox(self.frame, textvariable=self.selected_csv_file)
        self.csv_file_combobox.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_csv_file)
        self.browse_button.grid(row=0, column=2, pady=5, padx=5, sticky=tk.W)

        self.add_data_label = ttk.Label(self.frame, text="Enter data:")
        self.add_data_label.grid(row=1, column=0, pady=5, padx=5, sticky=tk.W)

        self.number_of_times_label = ttk.Label(self.frame, text="Number of times to add data:")
        self.number_of_times_label.grid(row=2, column=0, pady=5, padx=5, sticky=tk.W)

        self.number_of_times_entry = ttk.Entry(self.frame)
        self.number_of_times_entry.grid(row=2, column=1, pady=5, padx=5, sticky=tk.W)

        self.add_data_button = ttk.Button(self.frame, text="Add Data", command=self.add_data)
        self.add_data_button.grid(row=3, column=0, pady=10, padx=5, sticky=tk.W)

    def browse_csv_file(self):
        selected_file = filedialog.askopenfilename(initialdir=dir, title="Select CSV file", filetypes=[("CSV files", "*.csv")])
        if selected_file:
            self.selected_csv_file.set(selected_file)

    def add_data(self):
        try:
            number_of_times = int(self.number_of_times_entry.get())
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            return

        fieldnames = ["id", "comments"]

        for i in range(number_of_times):
            id_value = simpledialog.askstring("Enter ID", f"Enter the ID for data {i + 1}:")
            comments_value = simpledialog.askstring("Enter Comments", f"Enter the comments for data {i + 1}:")

            data = {"id": id_value, "comments": comments_value}

            try:
                with open(self.selected_csv_file.get(), mode='a', newline='') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    if file.tell() == 0:
                        writer.writeheader()
                    writer.writerow(data)

                print(f"Data added to '{self.selected_csv_file.get()}' successfully.")
            except Exception as e:
                print(f"Error: {e}")

class DriverCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Run Sentiment Analysis")

        self.frame = ttk.Frame(root, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.selected_csv_file = tk.StringVar()

        self.csv_file_label = ttk.Label(self.frame, text="Select CSV file:")
        self.csv_file_label.grid(row=0, column=0, pady=5, padx=5, sticky=tk.W)

        self.csv_file_combobox = ttk.Combobox(self.frame, textvariable=self.selected_csv_file)
        self.csv_file_combobox.grid(row=0, column=1, pady=5, padx=5, sticky=tk.W)

        self.browse_button = ttk.Button(self.frame, text="Browse", command=self.browse_csv_file)
        self.browse_button.grid(row=0, column=2, pady=5, padx=5, sticky=tk.W)

        self.run_analysis_button = ttk.Button(self.frame, text="Run Analysis", command=self.run_analysis)
        self.run_analysis_button.grid(row=1, column=0, pady=10, padx=5, sticky=tk.W)

    def browse_csv_file(self):
        selected_file = filedialog.askopenfilename(initialdir=dir, title="Select CSV file", filetypes=[("CSV files", "*.csv")])
        if selected_file:
            self.selected_csv_file.set(selected_file)

    def run_analysis(self):
        try:
            selected_csv_file = self.selected_csv_file.get()
            if not selected_csv_file:
                print("Please select a CSV file.")
                return

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
        MODEL = f"cardiffnlp/twitter-roberta-base-sentiment"
        tokenizer = AutoTokenizer.from_pretrained(MODEL)
        model = AutoModelForSequenceClassification.from_pretrained(MODEL)
        for x in column_data:
            sia = SentimentIntensityAnalyzer()
            print("Vader Analysis Result for statement-\n ", x, "---->")
            print(sia.polarity_scores(x))
            res = sia.polarity_scores(x)
            if 'compound' in res:
                res = res['compound']
                sum += res
                print(res)

            example = x
            encoded_text = tokenizer(example, return_tensors='pt')
            output = model(**encoded_text)
            scores = output[0][0].detach().numpy()
            scores = softmax(scores)
            scores_dict = {
                'roberta_neg': scores[0],
                'roberta_neu': scores[1],
                'roberta_pos': scores[2]
            }
            print("Roberta Analysis Result for statement-\n ", x, "---->")
            print(scores_dict)

        sentiment_value = sum / len(column_data)
        print('The polarity score using Vader Analysis method of the ', selected_csv_file, ' is ', sentiment_value)


def createNewBrand(brand_name):
    brand_name = brand_name + ".csv"
    csv_file_name = brand_name
    with open(dir + csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "comments"])
        writer.writeheader()
    print(f"Empty CSV file '{csv_file_name}' created successfully.")


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


# def createNewBrand(brand_name):
#     brand_name = brand_name+".csv"
#     csv_file_name = brand_name
#     with open(dir+csv_file_name, mode='w', newline='') as file:
#         writer = csv.DictWriter(file, fieldnames=["id", "comments"])
#         writer.writeheader()
#     print(f"Empty CSV file '{csv_file_name}' created successfully.")


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

def main():
    root = tk.Tk()
    app = SentimentAnalysisApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
