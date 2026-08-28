// Predict button functionality (on the Predict Page)
document.getElementById('predictButton').addEventListener('click', async function() {
    const title = document.getElementById('title').value;
    const body = document.getElementById('body').value;

    if (!title || !body) {
        alert("Title and body are required.");
        return;
    }

    // Call the /api/predict endpoint
    const response = await fetch('/api/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ title, body }),
    });

    const data = await response.json();

    if (response.ok) {
        // Display predicted label and confidence
        document.getElementById('predictedLabel').textContent = data.label;
        document.getElementById('confidence').textContent = data.confidence;
    } else {
        alert("Error: " + data.error);
    }
});