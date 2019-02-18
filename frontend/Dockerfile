FROM nginx:1.14

RUN apt update && apt upgrade -y
RUN apt install -y curl gnupg apt-transport-https
RUN curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | apt-key add -
RUN echo "deb https://dl.yarnpkg.com/debian/ stable main" | tee /etc/apt/sources.list.d/yarn.list

RUN apt update && apt install -y yarn
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt install -y nodejs

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
