import joblib
from preprocess import preprocess_text

# Load the model and vectorizer
model = joblib.load("final_random_forest_model.pkl")
vectorizer = joblib.load("final_tfidf_vectorizer.pkl")
def predict_label(title, body):
    """Predict the label and confidence for the given title and body."""
    combined_text = preprocess_text(title + " " + body)
    vectorized_text = vectorizer.transform([combined_text])

    # Predict label and confidence
    probabilities = model.predict_proba(vectorized_text)  # Get probabilities for each class
    predicted_index = probabilities.argmax()
    confidence = probabilities[0, predicted_index] * 100  # Convert to percentage

    return model.classes_[predicted_index], confidence

