FROM node:20-alpine

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies using `npm ci` for consistency
RUN npm ci

# Copy the rest of the application
COPY . .

# Expose the port
EXPOSE 3000

# Set the default command to run the development server
CMD ["npm", "run", "dev"]