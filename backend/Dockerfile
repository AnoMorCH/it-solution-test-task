# Pull official base image.
FROM python:3.11.4-slim-buster

# Set environment variables.
WORKDIR /usr/src/backend

# Set environment variables.
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install system dependecies.
RUN apt-get update && apt-get install -y netcat

# Install imagemagick to allow downloading of mp4 files.
RUN apt-get install -y imagemagick
RUN cat /etc/ImageMagick-6/policy.xml | sed 's/none/read,write/g'> /etc/ImageMagick-6/policy.xml

# Install dependecies.
RUN pip install --upgrade pip
COPY ./requirements.txt . 
RUN pip install -r requirements.txt

# Copy entrypoint.sh.
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/backend/entrypoint.sh
RUN chmod +x /usr/src/backend/entrypoint.sh

# Copy project.
COPY . .

# Run entrypoint.sh.
ENTRYPOINT ["/usr/src/backend/entrypoint.sh"]