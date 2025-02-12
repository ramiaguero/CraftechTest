FROM node:16

WORKDIR /app/frontend

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm install

# Copiar el resto del código
COPY . .

# Construir la aplicación
RUN npm run build

# Instalar serve
RUN npm install -g serve

# Exponer el puerto 3000 (para coincidir con docker-compose)
EXPOSE 3000

# Servir la aplicación
CMD ["serve", "-s", "build", "-l", "3000"]