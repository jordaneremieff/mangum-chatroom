# mangum-chatroom

**Work in Progress**

An example ASGI chatroom application and deployment for AWS Lambda & API Gateway. 

**IMPORTANT**

The WebSocket support demonstrated in this example is currently only available in the working branch for WebSocket pubsub in this PR: https://github.com/erm/mangum/pull/122. It is in a very experimental/unfinished state atm, so be careful if you attempt to run it.

## Requirements

- Python 3.8
- [Starlette](https://www.starlette.io/)
- [Serverless Framework](https://github.com/serverless/serverless)
- A WebSocket DSN, either S3 (boto3) or Redis (redis-py)
