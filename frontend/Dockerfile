# Use Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package files
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy frontend code
COPY . .

# Expose frontend port
EXPOSE 5173

# Run the frontend
CMD ["npm", "run", "dev", "--", "--host"]
