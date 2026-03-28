# ── Etapa 1: build ───────────────────────────────────────────────────────────
FROM node:20-alpine AS builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build

# ── Etapa 2: serve ────────────────────────────────────────────────────────────
FROM nginx:alpine

# Copiamos el build de Vite
COPY --from=builder /app/dist /usr/share/nginx/html

# Configuración de Nginx con proxy al backend y SPA fallback
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
