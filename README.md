
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
```


    