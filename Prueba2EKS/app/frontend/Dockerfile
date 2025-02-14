# Use Node.js as the base image
FROM node:16

# Set the working directory
WORKDIR /app/frontend

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the entire frontend code
COPY . .

# Build the React app
RUN npm run build

# Install `serve` globally (for serving the React build)
RUN npm install -g serve

# Expose the port the app runs on
EXPOSE 3000

# Start the frontend using `serve`
CMD ["serve", "-s", "build", "-l", "3000"]
