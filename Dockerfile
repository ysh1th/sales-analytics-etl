FROM python:3.11-slim

RUN apt-get update && apt-get install -y postgresql-client netcat-openbsd bash && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy everything (root and data_producers folder)
# COPY ./run_producers.py ./run_producers.py
# COPY ./data_producers ./data_producers
COPY . .
# Install any Python dependencies (if you have requirements.txt)
# (Optional, if you have one)
# COPY ./requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x scripts/*.sh

# Run the producer runner
CMD ["python", "run_producers.py"]
