# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Set environment variables
ENV BASE_URL http://backend:8000

# Expose port for Streamlit
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "frontend.py", "--server.port", "8501"]
