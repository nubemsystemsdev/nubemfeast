# ==============================================================================
# Dockerfile - Nubem Systems Standard
# Multi-stage build optimizado para producción
# ==============================================================================

# Stage 1: Dependencies
FROM node:20-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production && npm cache clean --force

# Stage 2: Builder
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build --if-present
RUN npm prune --production

# Stage 3: Production
FROM node:20-alpine AS runner
WORKDIR /app

LABEL org.opencontainers.image.source="https://github.com/nubemsystemsdev/[NOMBRE_PROYECTO]"

ENV NODE_ENV=production
ENV PORT=8080

# Usuario no-root
RUN addgroup --system --gid 1001 nodejs && \
    adduser --system --uid 1001 appuser

COPY --from=builder --chown=appuser:nodejs /app/node_modules ./node_modules
COPY --from=builder --chown=appuser:nodejs /app/dist ./dist
COPY --from=builder --chown=appuser:nodejs /app/package.json ./

USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["node", "dist/index.js"]
