FROM node:20-alpine

WORKDIR /app

# Copy package files và cài đặt dependencies
COPY package*.json ./
RUN npm install

# Copy toàn bộ source code
COPY . .

EXPOSE 5173

# Mặc định chạy dev server, lắng nghe mọi IP
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]
