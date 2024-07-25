# Use the Python 3.10 image as the base image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy the poetry configuration files to the container
COPY pyproject.toml poetry.lock ./

# Install poetry and configure it to not create a virtual environment
RUN pip install poetry
RUN poetry config virtualenvs.create false

# Install the dependencies specified in the pyproject.toml file
RUN poetry install --no-interaction --no-ansi

# Copy the entire project directory to the container
COPY . .

EXPOSE 5000

# CMD ["python", "assignment/main.py"]