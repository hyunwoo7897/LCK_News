FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the entire application directory into the container
COPY . .

# Set the PYTHONPATH environment variable to include the current directory
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Set other environment variables
ENV PYTHONUNBUFFERED 1
ENV OPENAI_API_KEY 'sk-proj-OYPQSYErvElP3Hkl7vqhT3BlbkFJZgKADqTwdsEoqGXBqwrP'

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the FastAPI app
EXPOSE 8000

# Command to run the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
