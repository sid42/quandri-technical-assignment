# Use a lightweight base image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Install Chrome and necessary dependencies
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    && rm -rf /var/lib/apt/lists/*

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get install -y \
    google-chrome-stable

# Copy the requirements file
COPY requirements.txt .

# Install the dependencies
RUN pip install -r requirements.txt

RUN webdrivermanager chrome

# Copy the test files to the container
COPY . .

# Set the entrypoint command to run the tests
CMD ["python3", "main.py"]