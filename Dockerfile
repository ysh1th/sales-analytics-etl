FROM python:3.13-alpine

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

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the producer runner
CMD ["python", "run_producers.py"]
