
FROM python:3.13.0

ENV PYTHONBUFFERED=1

# Set the working directory within the container to /app for any subsequent commands
WORKDIR /code

# Copy the entire current directory contents into the container at /app
COPY requirements.txt .

# Install dependencies from the requirements.txt file to ensure our Python environment is ready
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
# Set the command to run our web service using Gunicorn, binding it to 0.0.0.0 and the PORT environment variable
CMD ["python", "manage.py", "runserver"]

# Inform Docker that the container listens on the specified network port at runtime
EXPOSE ${PORT}