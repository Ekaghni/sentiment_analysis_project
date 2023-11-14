import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Load your CSV file into a DataFrame
df = pd.read_csv('C://Users//ekagh//OneDrive//Desktop//python_practice//Reviews.csv')

# Assuming a threshold of 4 for positive sentiment
df['Sentiment'] = df['Score'].apply(lambda x: 'positive' if x >= 3 else 'negative')

# Use numeric labels for SVM classifier
df['Sentiment'] = df['Sentiment'].map({'positive': 1, 'negative': 0})

# Split the data into training and testing sets
train_data, test_data, train_labels, test_labels = train_test_split(
    df['Text'], df['Sentiment'], test_size=0.2, random_state=42
)

# Convert text data to numerical features using TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=5000)
train_features = tfidf_vectorizer.fit_transform(train_data)
test_features = tfidf_vectorizer.transform(test_data)

# Train a Support Vector Machine (SVM) classifier
svm_classifier = SVC(kernel='linear')
svm_classifier.fit(train_features, train_labels)

# Predict sentiments on the test set
predictions = svm_classifier.predict(test_features)

# Evaluate the model
accuracy = accuracy_score(test_labels, predictions)
print(f"Accuracy: {accuracy:.2f}")

print("\nClassification Report:")
print(classification_report(test_labels, predictions))
