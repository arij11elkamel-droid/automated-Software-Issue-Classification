FROM python:3.11-slim


# Install dependencies for building scikit-learn and other Python packages
RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    python3-dev \
    python3-distutils \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Create /app directory
RUN mkdir -p /app

WORKDIR /app

# Upgrade pip, setuptools, and wheel to ensure compatibility
RUN pip install --upgrade pip setuptools wheel

# Copy the current directory contents into the container at /app
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# Download required NLTK resources
RUN python -m nltk.downloader punkt stopwords wordnet

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Expose port 5000 for Flask app
EXPOSE 5000

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]

