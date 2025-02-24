# Stage 1: Build stage
FROM node:16 AS build

# Set the working directory inside the container
WORKDIR /frontend-react-js

# Copy package.json and package-lock.json
COPY package*.json .

# Install dependencies
RUN npm install

# Copy the rest of the application code into the container
COPY . .

# Build the React application
RUN npm run build

# Stage 2: Final stage
FROM nginx:alpine

# Set the working directory inside the container
WORKDIR /usr/share/nginx/html

# Copy the built application from the build stage
COPY --from=build /frontend-react-js/build .

# Expose the port the app will run on
EXPOSE 80

# Command to run the Nginx server
CMD ["nginx", "-g", "daemon off;"]