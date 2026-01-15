# -----------------------------
# Base image
# -----------------------------
FROM python:3.13-slim

# -----------------------------
# Environment setup
# -----------------------------
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# -----------------------------
# Working directory
# -----------------------------
WORKDIR /app

# -----------------------------
# System dependencies (minimal)
# -----------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# Python dependencies
# -----------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------
# Copy project
# -----------------------------
COPY . .

# -----------------------------
# Expose Gradio port
# -----------------------------
EXPOSE 7860

# -----------------------------
# Run application
# -----------------------------
CMD ["python", "main.py"]
