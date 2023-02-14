FROM node:14.16.0-alpine3.10

# Set working directory
WORKDIR /app

# Set environment variables 
ENV NUXT_HOST 0.0.0.0

# Copy directory
COPY . .

# Install dependencies
RUN npm install --save
