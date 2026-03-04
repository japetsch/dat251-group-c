FROM node:lts-alpine AS builder

RUN mkdir /app
WORKDIR /app

ADD package*.json .
RUN npm ci

ADD . .

RUN npm run build

FROM node:lts-alpine AS final

RUN mkdir /app
WORKDIR /app

# Create non-root user
RUN addgroup --system --gid 1001 appgroup && \
    adduser --system --uid 1001 --ingroup appgroup appuser

COPY --from=builder --chown=appuser:appgroup /app/build .

USER appuser
EXPOSE 3000

CMD [ "node", "." ]
