import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from mailSenderClass import EmailSender  # Import the EmailSender class
from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import hashlib

class CSVFileHandler(FileSystemEventHandler):
    def __init__(self, email_sender, csv_file_path):
        self.email_sender = email_sender
        self.csv_file_path = csv_file_path
        self.last_hash = self.calculate_file_hash()

    def calculate_file_hash(self):
        with open(self.csv_file_path, "rb") as f:
            content = f.read()
            return hashlib.sha256(content).hexdigest()

    def on_any_event(self, event):
        if event.src_path == self.csv_file_path:
            print(f"Change detected in {event.src_path}")
            new_hash = self.calculate_file_hash()
            if new_hash != self.last_hash:
                print("Calling driverCode() function...")
                self.driverCode("my_reviews.csv")
                self.last_hash = new_hash

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

def run_watchdog(csv_file_path, email_sender):
    event_handler = CSVFileHandler(email_sender, csv_file_path)
    observer = Observer()
    observer.schedule(event_handler, path='.', recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)  # Check for changes every 5 seconds
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    # Replace with your own email and app password
    sender_username = "your_email@gmail.com"
    sender_password = "your_app_password"

    # Create an instance of EmailSender
    email_sender = "xyz"
    # Specify the CSV file to monitor
    csv_file_to_monitor = "my_reviews.csv"  # Replace with the actual CSV file

    run_watchdog(csv_file_to_monitor, email_sender)
