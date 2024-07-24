FROM python:3.10

# Install system dependencies
RUN apt update

# Install poerty
RUN apt install -y pipx
RUN pipx ensurepath
RUN pipx install poetry

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file to the container
COPY . .

# Install the Python dependencies
RUN poetry install

# Expose the port your application will be running on
EXPOSE 5000

# Set the command to run the Gunicorn server
CMD ["python", "assignment/main.py"]