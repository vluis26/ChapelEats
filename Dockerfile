FROM python:3.10.6

WORKDIR /app

# Copy the application code to the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Start the Flask app using gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "main:app"]
