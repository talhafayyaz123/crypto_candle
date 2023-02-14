FROM python:3.7-alpine

# Set working directory
WORKDIR /app

# Set environment variables 
ENV FLASK_RUN_HOST 0.0.0.0

# Copy directory
COPY . .

# Install dependencies 
RUN apk add --no-cache gcc musl-dev linux-headers libffi-dev g++
RUN pip3 install -r requirements.txt
