# Use an official Python runtime as a parent image
FROM python:3.11

# Install ODBC driver dependencies
RUN apt-get update && apt-get install -y unixodbc unixodbc-dev

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run app.py when the container launches
CMD ["python3", "app.py"]