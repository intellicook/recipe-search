# Pull official base image
FROM python:3.12.2-slim

# Set work directory
WORKDIR /usr/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --no-compile --no-cache-dir --upgrade pip
RUN pip install --no-compile --no-cache-dir numpy==2.1.2 pillow==11.0.0 Jinja2==3.1.4
RUN pip install --no-compile --no-cache-dir \
    torch==2.5.1 torchaudio==2.5.1 torchvision==0.20.1 \
    -i https://download.pytorch.org/whl/cpu
COPY ./requirements.txt .
RUN pip install --no-compile --no-cache-dir -r requirements.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/app/entrypoint.sh
RUN chmod +x /usr/app/entrypoint.sh

# Copy project
COPY . .

# Run entrypoint.sh
ENTRYPOINT ["/usr/app/entrypoint.sh"]
