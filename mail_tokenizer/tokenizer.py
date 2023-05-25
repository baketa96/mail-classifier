import spacy
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import nltk
import ssl
import warnings
import joblib
warnings.filterwarnings("ignore")
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context
nltk.download('wordnet')
import random
from nltk.corpus import wordnet as wn


# Load the SpaCy English model
nlp = spacy.load('en_core_web_sm')

# 0 is maintenance, 1 it is down
data_df = pd.read_excel('/Users/aleksandar.bajceta/src/mail-classifier/File_for_training.xlsx')

# Split data into input (X) and target (y)
X = data_df['Text'].values
y = data_df['Is_incident'].values

print(data_df['Is_incident'].value_counts())

# Split data into training and testing sets // later we can check how to create fake data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define the SpaCy tokenizer// here we are going to play with tokenization and check our results
def spacy_tokenizer(text):
    tokens = nlp(text)
    return [token.lemma_.lower() for token in tokens if not token.is_punct and not token.is_stop]

# Define the models to evaluate
models = [
    ('LinearSVC', LinearSVC()),
    ('Random Forest', RandomForestClassifier()),
    ('Naive Bayes', MultinomialNB()),
    ('Logistic Regression', LogisticRegression()),
    ('AdaBoost', AdaBoostClassifier()),
    ('GradientBoosting', GradientBoostingClassifier()),
    ('SGD', SGDClassifier())
]

# Create a pipeline with SpaCy tokenizer and TF-IDF vectorizer // here we are going to play with models that we are going to use
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(tokenizer=spacy_tokenizer)),
    ('clf', None)
])

# # Train the model
# pipeline.fit(X_train, y_train)

# # Make predictions on the test set
# y_pred = pipeline.predict(X_test)

# # Calculate accuracy
# accuracy = accuracy_score(y_test, y_pred)
# print("Accuracy:", accuracy)

for model_name, model in models:
    pipeline.set_params(clf=model)  # Set the classifier for the current model
    scores = cross_val_score(pipeline, X, y, cv=5)  # Perform cross-validation
    print(f"{model_name} Accuracy: {scores.mean():.4f}")


# joblib.dump(pipeline, 'classification_model.joblib')


# Data augmentation for the specific label
augmented_X = []
augmented_y = []


target_label = '1'  # Label to increase the size

for text, label in zip(X_train, y_train):
    augmented_X.append(text)
    augmented_y.append(label)
    
    if label == 1:
        # Get synonyms for each word in the text
        tokens = text.split()
        synonyms = []
        for token in tokens:
            synsets = wn.synsets(token)
            if synsets:
                synonyms.append(random.choice(synsets).lemmas()[0].name())
            else:
                synonyms.append(token)
        
        # Create augmented texts by replacing words with synonyms
        augmented_text = ' '.join(synonyms)
        augmented_X.append(augmented_text)
        augmented_y.append(label)


# Extend the original training set with augmented data
X_train_extended = X_train.tolist() + augmented_X
y_train_extended = y_train.tolist() + augmented_y


df_new = pd.DataFrame(y_train_extended)

print(df_new.value_counts())


for model_name, model in models:
    pipeline.set_params(clf=model)  # Set the classifier for the current model
    scores = cross_val_score(pipeline, X_train_extended, y_train_extended, cv=5)  # Perform cross-validation
    print(f"{model_name} Accuracy with Augm Data: {scores.mean():.4f}")


df_new = pd.DataFrame(y_train_extended)

print(df_new.value_counts())

# Retrain the model with extended training set
pipeline.fit(X_train_extended, y_train_extended)

# Make predictions on the test set using the updated model
y_pred_extended = pipeline.predict(X_test)

# Calculate accuracy using the updated model
accuracy_extended = accuracy_score(y_test, y_pred_extended)
print("Accuracy (Extended):", accuracy_extended)