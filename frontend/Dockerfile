FROM node:22-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

ARG NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL

COPY . .
RUN npm run build

ENV NODE_ENV=production

EXPOSE 3000

CMD sh -c "npm start -- -p ${PORT:-3000}"
