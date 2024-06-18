FROM python:3.10.6

WORKDIR /app
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

WORKDIR /app/backend

CMD ["gunicorn", "-b", "0.0.0.0:5000", "main:app"]
