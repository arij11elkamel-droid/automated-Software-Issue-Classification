// script.js
// Submit button functionality (on the Correct Page)

  

document.getElementById('submitButton').addEventListener('click', async function() {
    
    const issue_id = document.getElementById('issue_id').value;
    const corrected_label = document.getElementById('corrected_label').value;

    if (!issue_id || !corrected_label) {
        alert("Issue ID and corrected label are required.");
        return;
    }
    // Fetch the issue details first to get the confidence
    const issueResponse = await fetch(`/api/predict/${issue_id}`);
    
    const issueData = await issueResponse.json();

    // Call the /api/correct endpoint
    const response = await fetch('/api/correct', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ issue_id, corrected_label }),
    });

    const data = await response.json();

    if (response.ok && issueResponse.ok) {
        document.getElementById('confidenceDisplay').textContent = `confidence of predicted label is : ${issueData.confidence}%`;
        document.getElementById('submissionResult').textContent = `Issue ${data.id} corrected successfully!`;

    } else if (!issueResponse.ok) {
        document.getElementById('submissionResult').textContent = `Error: Unable to fetch issue details.`;
        return;
    } else {
        document.getElementById('submissionResult').textContent = `Error: ${data.error}`;
        document.getElementById('confidenceDisplay').textContent = `N/A`;
    }
    
    
}); 






