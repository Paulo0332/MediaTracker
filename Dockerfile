# 1 - Selecting the base image
FROM python:3.12-slim

# 2 - Setting work directory inside the container
WORKDIR /usr/src/app

# 3 - Set environment variables for better python operation
ENV PYTHONUNBUFFERED 1

# 4 - Install netcat for the entrypoint script
RUN apt-get update && apt-get install -y netcat-traditional\
&& rm -rf /var/lib/apt/lists/*

# 5 - Copy dependencies list and install them
COPY requirements.txt /usr/src/app
RUN pip install --no-cache-dir -r requirements.txt

# 6 - Entrypoint script setup
COPY ./wait_for_db.sh /usr/src/app/
RUN chmod +x /usr/src/app/wait_for_db.sh

# 7 - Copy the rest of the application code
COPY . /usr/src/app

# 8 - Defines the wrapper program (wait_for_db script) that always run first
ENTRYPOINT [ "/usr/src/app/wait_for_db" ]

# 9 - Define the default arguments passed to the entrypoint
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]