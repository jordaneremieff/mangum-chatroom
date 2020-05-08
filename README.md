# mangum-example

An example ASGI application deployment for AWS Lambda & API Gateway.

**Work in Progress**

## Requirements

- Python 3.7
- [Serverless Framework](https://github.com/serverless/serverless)

### Setup

- Rename `serverless.yml.dist` to `serverless.yml`

- Edit the `serverless.yml` file, set a database name, username, and password:

```
  DB_NAME: <db name>
  DB_USERNAME: <username>
  DB_PASSWORD: <password>
```

- Save and deploy

```
sls deploy
```
