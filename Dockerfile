# Pull official base image
FROM python:3.12.2-slim

# Set work directory
WORKDIR /usr/app

# Install psycopg2 dependencies
RUN apt-get update \
    && apt-get -y install libpq-dev gcc

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/app/entrypoint.sh
RUN chmod +x /usr/app/entrypoint.sh

# Copy project
COPY . .

# Run entrypoint.sh
ENTRYPOINT ["/usr/app/entrypoint.sh"]
