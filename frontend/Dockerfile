FROM node:20-alpine

WORKDIR /app

# Copy package files first
COPY package.json ./
COPY tsconfig.json ./
COPY next.config.js ./
COPY postcss.config.mjs ./
COPY tailwind.config.ts ./

# Clear npm cache and install dependencies
RUN npm cache clean --force && \
    npm install

# Copy source code
COPY src ./src
COPY public ./public

# Expose port
EXPOSE 3000

CMD ["npm", "run", "dev"]
