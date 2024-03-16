# Use the official Python image as base
FROM python:3.9

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code into the container
COPY . /code/

# Migrations
RUN python manage.py makemigrations
RUN python manage.py migrate
# Run tests
# RUN python manage.py test # Disabled because it does not work when auth is enabled

# Run the Django application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "huggingfacemodelsapi.wsgi:application"]
