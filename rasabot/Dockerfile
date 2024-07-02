FROM python:3.10

# Set working directory
WORKDIR /code

# Copy requirements file
COPY ./requirements.txt /code/app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code
COPY . /code/app

# Make the start script executable
RUN chmod +x /code/app/start_servers.sh

# Set the start script as the entrypoint
ENTRYPOINT ["/code/app/start_servers.sh"]