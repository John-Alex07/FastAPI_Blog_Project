# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to allow external access
EXPOSE 80

# Define environment variable for MongoDB connection string
ENV MONGODB_URL mongodb+srv://admin:admin@demo.d6mozcq.mongodb.net/?retryWrites=true&w=majority

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
