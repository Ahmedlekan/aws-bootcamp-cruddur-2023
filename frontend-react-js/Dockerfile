# docker file

# Use the official Node.js image as the base image
FROM node:16

COPY . /frontend-react-js

WORKDIR /frontend-react-js

RUN npm install

EXPOSE ${PORT}

CMD ["npm", "start"]