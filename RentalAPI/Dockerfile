# Pull official base image
FROM python:3.9.6-alpine

# Set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install mysql dependencies
RUN apk update && apk add mysql-dev gcc python3-dev musl-dev

# Install dependencies
RUN pip3 install --upgrade pip
COPY RentalAPI/requirements.txt .
RUN pip3 install -r requirements.txt
RUN pip3 install gunicorn==20.1.0

# Copy the access token creation file
RUN pip3 install PyJWT>=2.8.0
COPY CoordinatesAPI/create_access_token.py .

# Copy entrypoint.sh
COPY RentalAPI/entrypoint.sh .
RUN sed -i 's/\r$//g' ./entrypoint.sh
RUN chmod +x ./entrypoint.sh

# Copy project
COPY RentalAPI .

# Run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
