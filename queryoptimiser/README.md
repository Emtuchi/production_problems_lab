# “Resolved N+1 query issues in a Node.js + PostgreSQL backend, adding indexes and eager loading to reduce API query time by ~97% on 100k+ records in Typescript and python

## Dependencies for TypeScript

- npm init -y

- npm install express sequelize pg pg-hstore faker

- npm install -D typescript ts-node-dev @types/node @types/express

## Run Typescript project

- npx ts-node src/seed.ts

- npx ts-node src/app.ts

## Dependencies For Python

- pip install fastapi uvicorn sqlalchemy faker

## Run python project

- uvicorn main:app --reload

- GET /users/1/orders

### Note: faker is used to simulate user data
