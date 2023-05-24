import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load the SpaCy English model
nlp = spacy.load('en_core_web_sm')

# 0 is maintenance, 1 it is down

data = [
    ("Important: Scheduled maintenance on our system tonight from 10 PM to 2 AM.",0),
    ("Service disruption notification: API service experiencing intermittent errors.", 1),
    ("Upcoming maintenance window: Our system will be unavailable on Sunday, 3rd July.", 0),
    ("Issue with API response times - please expect delays in data retrieval.", 1),
    ("Bank XYZ: Temporary downtime of our online services due to system upgrade.", 0),
    ("To ThirdPartyProviders using PSD2 APIs at Bankdata banks FYI we are currently experiencing disturbances in PSD2 APIs. PaymentServiceUsers experience error when trying to sign consent or payment with MitID. We send you an email as soon as status changes… Best regards", 1)
]

# Split data into input (X) and target (y)
X = [text for text, _ in data]
y = [label for _, label in data]

# Split data into training and testing sets // later we can check how to create fake data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the SpaCy tokenizer// here we are going to play with tokenization and check our results
def spacy_tokenizer(text):
    tokens = nlp(text)
    return [token.lemma_.lower() for token in tokens if not token.is_punct and not token.is_stop]


# Create a pipeline with SpaCy tokenizer and TF-IDF vectorizer // here we are going to play with models that we are going to use
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(tokenizer=spacy_tokenizer)),
    ('clf', LinearSVC())
])

# Train the model
pipeline.fit(X_train, y_train)

# Make predictions on the test set
y_pred = pipeline.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)