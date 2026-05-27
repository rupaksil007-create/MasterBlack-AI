FROM node:20-slim

WORKDIR /app

COPY frontend/package*.json ./
RUN npm install

COPY . .

WORKDIR /app/frontend

EXPOSE 3000

CMD ["npm", "run", "dev"]
