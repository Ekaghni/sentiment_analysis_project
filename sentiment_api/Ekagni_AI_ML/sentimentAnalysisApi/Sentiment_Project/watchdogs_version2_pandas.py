import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import pandas as pd
import csv
from mailSenderClass import EmailSender
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('vader_lexicon')

class CSVHandler(FileSystemEventHandler):
    def __init__(self, csv_path, column_to_watch):
        self.csv_path = csv_path
        self.column_to_watch = column_to_watch
        self.last_state = None


    def on_modified(self, event):
        if event.src_path.endswith('.csv'):
            current_state = pd.read_csv(self.csv_path)
            if self.last_state is not None:
                if not current_state.equals(self.last_state):
                    # CSV file has been modified
                    new_values = current_state[self.column_to_watch].values
                    print(f"Change detected in {self.column_to_watch} column. New values: {new_values}")
                    self.driverCode("C://Users//ekagh//OneDrive//Desktop//sentiment_analysis_project//sentiment_api//Ekagni_AI_ML//sentimentAnalysisApi//Sentiment_Project//csv_files//my_reviews.csv")
            else:
                # This is the initial check, print information about the initial state
                print(f"Initial state: {current_state[self.column_to_watch].values}")
                self.driverCode("C://Users//ekagh//OneDrive//Desktop//sentiment_analysis_project//sentiment_api//Ekagni_AI_ML//sentimentAnalysisApi//Sentiment_Project//csv_files//my_reviews.csv")

            self.last_state = current_state


    def driverCode(self, selected_csv_file):
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
        print('The polarity score of the ', selected_csv_file, ' is ', sentiment_value)
        self.send_email(sentiment_value, selected_csv_file)

    def send_email(self, sentiment_value, csv_file_name):
        ####################################################
        sender_username = "dmukherjee1316@gmail.com"
        sender_password = "rvsv keep chcm xoka"
        email_sender = EmailSender(sender_username, sender_password)
        email_subject = "Sentiment Value Change Alert"
        email_body = f"The content of the CSV file has changed. Now the brand value of {csv_file_name} is {sentiment_value}"
        recipient_email = "ekaghni.mukherjee@gmail.com"
        email_sender.send_email(email_subject, email_body, recipient_email)
        ####################################################

def observe_csv_changes(csv_path, column_to_watch, interval=3):
    event_handler = CSVHandler(csv_path, column_to_watch)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(interval)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    csv_path = "C://Users//ekagh//OneDrive//Desktop//sentiment_analysis_project//sentiment_api//Ekagni_AI_ML//sentimentAnalysisApi//Sentiment_Project//csv_files//my_reviews.csv"
    column_to_watch = "comments"
    observe_csv_changes(csv_path, column_to_watch)
