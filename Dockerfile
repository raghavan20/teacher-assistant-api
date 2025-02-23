# Use official Python 3.10 image
FROM python:3.10

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project into the container
COPY . .

# Set environment variables (optional, but can be overridden in docker-compose)
ENV DB_USER=postgres \
    DB_PASSWORD=GsWUnMeIInzKCeATVZctEQCnewxwCAFk \
    DB_HOST=interchange.proxy.rlwy.net \
    DB_PORT=54776 \
    DB_NAME=teaching_db

# Expose the port the app runs on (change if needed)
EXPOSE 5000

# Command to run the application
#CMD ["python", "app.py"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
