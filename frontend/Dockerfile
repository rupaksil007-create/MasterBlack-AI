FROM node:20-slim

WORKDIR /app/frontend

# Copy only frontend dependencies first for better caching
COPY frontend/package*.json ./
RUN npm install

# Copy only frontend source code to keep the container clean
COPY frontend/ .

EXPOSE 3000

# Next.js 16 handles Turbopack internally; no special flags needed
CMD ["npm", "run", "dev"]
