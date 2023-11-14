import tkinter as tk
from tkinter import ttk, messagebox
from nltk.sentiment import SentimentIntensityAnalyzer
import csv
import os
import nltk
nltk.download('vader_lexicon')

def driver_code(selected_csv_file):
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
    total_score = 0
    for x in column_data:
        sia = SentimentIntensityAnalyzer()
        print(sia.polarity_scores(x))
        res = sia.polarity_scores(x)
        if 'compound' in res:
            res = res['compound']
            total_score += res
            print(res)
    sentiment_value = total_score / len(column_data)
    print('The average polarity score is:', sentiment_value)
    messagebox.showinfo("Sentiment Analysis Result", f"The average polarity score is: {sentiment_value}")

def create_new_brand(brand_name):
    brand_name = brand_name + ".csv"
    csv_file_name = brand_name
    with open(csv_file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "comments"])
        writer.writeheader()
    messagebox.showinfo("CSV File Created", f"Empty CSV file '{csv_file_name}' created successfully.")

def add_data_to_csv(selected_csv_file, input_id, input_comments, times_to_add):
    fieldnames = ["id", "comments"]
    
    for i in range(times_to_add):
        id_value = input_id.get()
        comments_value = input_comments.get()
        
        data = {"id": id_value, "comments": comments_value}
        try:
            with open(selected_csv_file, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                if file.tell() == 0:
                    writer.writeheader()
                writer.writerow(data)
            messagebox.showinfo("Data Addition Result","Comment added successfully..")
            print(f"Data added to '{selected_csv_file}' successfully.")
        except Exception as e:
            print(f"Error: {e}")

def menu_nltk():
    root = tk.Tk()
    root.title("Sentiment Analysis System")

    # Set minimum size for the window
    root.minsize(500, 300)

    def execute_menu():
        selected_index = combo_box.get()
        if selected_index == "Create a new brand":
            brand_name = input_brand_name.get()
            create_new_brand(brand_name)
        elif selected_index == "Add comments to existing brands":
            selected_csv_file = combo_box_existing_brands.get()
            times_to_add = int(input_times_to_add.get())
            add_data_to_csv(selected_csv_file, input_id, input_comments, times_to_add)
        elif selected_index == "Run sentiment analysis on brands":
            selected_csv_file = combo_box_existing_brands.get()
            driver_code(selected_csv_file)

    label_brand_name = tk.Label(root, text="Brand Name:")
    label_brand_name.grid(row=0, column=0, padx=5, pady=5)

    input_brand_name = tk.Entry(root)
    input_brand_name.grid(row=0, column=1, padx=5, pady=5)

    button_execute_menu = tk.Button(root, text="Execute", command=execute_menu)
    button_execute_menu.grid(row=1, column=0, columnspan=2, pady=10)

    combo_box_values = ["Select an option", "Create a new brand", "Add comments to existing brands",
                        "Run sentiment analysis on brands"]
    combo_box = ttk.Combobox(root, values=combo_box_values)
    combo_box.set(combo_box_values[0])
    combo_box.grid(row=2, column=0, columnspan=2, pady=10)

    label_existing_brands = tk.Label(root, text="Existing Brands:")
    label_existing_brands.grid(row=3, column=0, padx=5, pady=5)

    csv_files = [file for file in os.listdir() if file.endswith(".csv")]
    combo_box_existing_brands = ttk.Combobox(root, values=csv_files)
    combo_box_existing_brands.set(csv_files[0] if csv_files else "")
    combo_box_existing_brands.grid(row=3, column=1, padx=5, pady=5)

    # Frame for the add_data_to_csv function
    frame_add_data = tk.Frame(root)
    frame_add_data.grid(row=4, column=0, columnspan=2, pady=10)

    label_id = tk.Label(frame_add_data, text="ID:")
    label_id.grid(row=0, column=0, padx=5, pady=5)

    input_id = tk.Entry(frame_add_data)
    input_id.grid(row=0, column=1, padx=5, pady=5)

    label_comments = tk.Label(frame_add_data, text="Comments:")
    label_comments.grid(row=1, column=0, padx=5, pady=5)

    input_comments = tk.Entry(frame_add_data)
    input_comments.grid(row=1, column=1, padx=5, pady=5)

    label_times_to_add = tk.Label(frame_add_data, text="Number of Times to Add:")
    label_times_to_add.grid(row=2, column=0, padx=5, pady=5)

    input_times_to_add = tk.Entry(frame_add_data)
    input_times_to_add.grid(row=2, column=1, padx=5, pady=5)

    root.mainloop()

menu_nltk()
