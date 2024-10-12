# Use the official Python image
FROM python:3.11-slim



RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev gcc

# create directory
RUN mkdir fastapi_app

# Set the working directory
WORKDIR /fastapi_app

# Copy requirements file
COPY pyproject.toml ./

# Install dependencies
RUN pip install poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-root --without dev

# Copy the rest of the app
COPY . .


RUN chmod a+x docker/*.sh

# Expose the port the app will run on
#EXPOSE 8000

# Command to run the app
#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
