FROM nginx:mainline-alpine3.18-slim

RUN apk add nodejs npm yarn

RUN mkdir frontend
WORKDIR frontend

COPY package.json yarn.lock ./

RUN yarn install
COPY tsconfig.json webpack.config.js ./

COPY css ./css
COPY ts  ./ts
COPY index.html .

RUN yarn run build

RUN cp index.html build

COPY nginx.conf /etc/nginx/nginx.conf
