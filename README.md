
# Sentiment Analysis Project

This project facilitates the calculation of sentiment values based on comments through the utilization of NLTK, Transformers, VADER, and pre-trained models such as RoBERTa. It generates a dictionary that includes positive, negative, neutral, and compound scores. Simply input the comments into a CSV file, and you can then compare the sentiment values produced by VADER and RoBERTa. Any alteration in sentiment values will trigger a mailing system, providing real-time updates via email through the implementation of Watchdogs and SMTP.

To enhance functionality, I have developed a REST API using Django, enabling the addition of comments to the CSV file and retrieval of sentiment values. Additionally, to optimize accessibility, a tunneling network has been established using Cloudflare, allowing access to the API from any location worldwide.


## Installation

Step 1)

```bash
  Install Python 3.10.0
  Install git bash
  Install Visual Studio Code
```

Step 2)

```bash
  git clone xyz.com
```

Step 3)

```bash
  cd Sentiment_Analysis_project
  pip install -r requirements.txt
```


    
## Running Via Terminal



```bash
  Step 1) Open start_auto_mailer.bat file in vs code

  Step 2) Change the directory of the start_auto_mailer.bat according to your path.

  Step 3) Run start_auto_mailer.bat

  Step 4) Open Main_code folder using vs code

  Step 5) Navigate to nltk_trial.py and change the dir path with the Main_code folder path.

  Step 6) Run nltk_trial.py
```
## Running Via Gui

```bash
  Step 1) Open Main_code folder using vs code

  Step 2) Navigate to gui_v2.py and change the dir path with the Main_code folder path.

  Step 3) Run gui_v2.py
```
## Running API Locally


```bash
  Step 1) Open sentiment_api folder

  Step 2) Run py manage.py runserver 0.0.0.0:3000

  Step 3) This will run your api on port 3000 of localhost
```
## API Reference

#### Post id, comments, brandname

```http
  POST http://127.0.0.1:3000/sentimentAnalysisApi/image/
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `image0` | `image file` | **Required**. Select the image |
| `option` | `int` | **Required**. 1) Get Sentiment Value of A Brand        2) Create new brand 3) Add id and comments |
| `selected_csv_file` | `str` | **Required**. Enter the csv file name |
| `brandName` | `str` | **Required**. Enter the name of the brand you want to create |
| `id_value` | `int` | **Required**. Enter the csv id's |
| `comments_value` | `str` | **Required**. Enter the comment on brand |


## Tunnelling API Using Cloud Flared

```bash
  Step 1) Open sentiment_api folder

  Step 2) Run py manage.py runserver 0.0.0.0:3000

  Step 3) Run cloudflared tunnel --url http://127.0.0.1:3000

  Step 4) You will get a temporary endpoint link from cloudflared and through this link you can access the api from anywhere around the world
```