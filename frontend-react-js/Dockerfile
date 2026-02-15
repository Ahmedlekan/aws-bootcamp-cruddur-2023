# Stage 1: Build stage
FROM node:20-alpine AS build
# Set working directory
WORKDIR /app
# Copy only package.json and package-lock.json first for caching
COPY package*.json ./
# Install dependencies
RUN npm ci
# Copy the entire app source code
COPY . .
# Build the React application
RUN npm run build

# Stage 2: Serve with Nginx
FROM nginx:alpine
# Copy the built React app from the previous stage
COPY --from=build /app/build /usr/share/nginx/html
# Copy custom Nginx configuration (optional but recommended)
COPY nginx.conf /etc/nginx/conf.d/default.conf
# Expose the port the app will run on
EXPOSE 80
# Run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]
