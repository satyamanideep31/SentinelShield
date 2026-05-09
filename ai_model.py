from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

training_data = [
    "gun attack in area",
    "cyber hacking detected",
    "normal community meeting",
    "suspicious person found",
    "bank fraud attempt",
    "peaceful event",
    "phishing email attack",
    "weapon seen near school"
]

labels = [
    "High",
    "High",
    "Low",
    "Medium",
    "High",
    "Low",
    "High",
    "High"
]

vectorizer = CountVectorizer()

X = vectorizer.fit_transform(training_data)

model = MultinomialNB()

model.fit(X, labels)

def predict_threat(text):

    transformed = vectorizer.transform([text])

    result = model.predict(transformed)

    return result[0]