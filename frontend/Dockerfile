# Front-end React (servidor de desenvolvimento do Vite). Usado pelo docker-compose.yml da raiz.
FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

# --host para o Vite aceitar ligações de fora do contentor.
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
