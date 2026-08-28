from flask import Flask, request, jsonify,render_template 
import uuid
from prometheus_client import Counter, Gauge, Histogram, Summary, generate_latest, CONTENT_TYPE_LATEST
from model import predict_label
from database import save_prediction, update_corrected_label, fetch_issue
from preprocess import is_english

app = Flask(__name__, static_folder='assets', template_folder='templates')


# Prometheus Metrics
accuracy = Gauge('accuracy', 'Model Accuracy')
avg_prediction_confidence = Summary('average_prediction_confidence', 'Average Prediction Confidence')
predictions_per_category = Counter('predictions_per_category', 'Number of Predictions per Category', ['category'])
correct_predictions_per_category = Counter('correct_predictions_per_category', 'Correct Predictions per Category', ['category'])
incorrect_predictions_per_category = Counter('incorrect_predictions_per_category', 'Incorrect Predictions per Category', ['category'])

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Predict page route
@app.route('/predict')
def predict():
    return render_template('predict.html')

# Correct page route
@app.route('/correct')
def correct():
    return render_template('correct.html')

@app.route('/api/predict/<issue_id>', methods=['GET'])
def get_issue(issue_id):
    issue = fetch_issue(issue_id)
    if issue:
        return jsonify(issue), 200
    else:
        return jsonify({"error": "Issue ID not found"}), 404

@app.route('/metrics', methods=['GET'])
def metrics():
    """Expose Prometheus metrics."""
    return generate_latest(), 200, {'Content-Type': CONTENT_TYPE_LATEST}

# Endpoint: Predict issue type
@app.route('/api/predict', methods=['POST'])
def predict_issue():
    data = request.get_json()
    title = data.get('title', '')
    body = data.get('body', '')

    # Check for non-English input
    if not is_english(title) or not is_english(body):
        return jsonify({"error": "Non-English text detected. Please provide text in English."}), 400

    # Check if title or body is empty
    if not title:
        return jsonify({"error": "Title is empty"}), 400
    if not body:
        return jsonify({"error": "Body is empty"}), 400

    # Generate unique issue ID
    issue_id = str(uuid.uuid4())

    # Predict label using the model
    predicted_label,confidence = predict_label(title, body)

    # Save prediction to the database
    save_prediction(issue_id, title, body, predicted_label,confidence)

    # Update Metrics
    predictions_per_category.labels(category=predicted_label).inc()
    avg_prediction_confidence.observe(confidence)

    # Return response
    response = {
        "id": issue_id,
        "label": predicted_label,
        "confidence": f"{confidence:.2f}%"
    }
    return jsonify(response), 200

# Endpoint: Correct issue label
@app.route('/api/correct', methods=['POST'])
def correct_issue():
    data = request.get_json()
    issue_id = data.get('issue_id', '')
    corrected_label = data.get('corrected_label', '')

    # Fetch and update issue
    issue = fetch_issue(issue_id)
    if  issue:
       update_corrected_label(issue_id, corrected_label)
       # Update Metrics
       if corrected_label == issue['predicted_label']:
            correct_predictions_per_category.labels(category=corrected_label).inc()
       else:
            incorrect_predictions_per_category.labels(category=issue['predicted_label']).inc()
            
       response = {
        "id": issue_id,
        "corrected_label": corrected_label
    }
       return jsonify(response), 200
    else :
        return jsonify({"error": "Issue ID not found"}), 404
    

# Run the application
#if __name__ == '__main__':
#   app.run(debug=True)
# Run the application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')