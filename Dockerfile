# Pull official base image
FROM python:3.12.2-slim

# Set work directory
WORKDIR /usr/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Run entrypoint.sh
ENTRYPOINT ["/usr/app/entrypoint.sh"]
