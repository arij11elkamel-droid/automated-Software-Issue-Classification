from flask import Flask, request, jsonify
import uuid
from model import predict_label
from database import save_prediction, update_corrected_label, fetch_issue

app = Flask(__name__)

# Endpoint: Predict issue type
@app.route('/api/predict', methods=['POST'])
def predict_issue():
    data = request.get_json()
    title = data.get('title', '')
    body = data.get('body', '')

    # Generate unique issue ID
    issue_id = str(uuid.uuid4())

    # Predict label using the model
    predicted_label = predict_label(title, body)

    # Save prediction to the database
    save_prediction(issue_id, title, body, predicted_label)

    # Return response
    response = {
        "id": issue_id,
        "label": predicted_label
    }
    return jsonify(response), 200

# Endpoint: Correct issue label
@app.route('/api/correct', methods=['POST'])
def correct_issue():
    data = request.get_json()
    issue_id = data.get('id', '')
    corrected_label = data.get('label', '')

    # Fetch and update issue
    issue = fetch_issue(issue_id)
    if not issue:
        return jsonify({"error": "Issue ID not found"}), 404

    update_corrected_label(issue_id, corrected_label)

    response = {
        "id": issue_id,
        "corrected_label": corrected_label
    }
    return jsonify(response), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
