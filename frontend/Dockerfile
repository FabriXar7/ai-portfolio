# Etapa de construcción
FROM node:20-slim AS builder

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de paquetes
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar el resto de las aplicaciones
COPY . .

# Desarrollar la aplicacion
RUN npm run build

# Etapa de Producion
FROM nginx:alpine

# Copiar comun nginx configuracion para manejar ruteo SPA 
RUN echo 'server { \
    listen 80; \
    location / { \
        root /usr/share/nginx/html; \
        index index.html; \
        try_files $uri $uri/ /index.html; \
    } \
}' > /etc/nginx/conf.d/default.conf

# Copiar activos construidos desde la etapa de construcción
COPY --from=builder /app/dist /usr/share/nginx/html

# Exponer puerto 80
EXPOSE 80

# Iniciar nginx
CMD ["nginx", "-g", "daemon off;"]
