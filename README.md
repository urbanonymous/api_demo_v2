# api_demo_v2

This API is the result of a hiring exercise.

The purpose of this API is to allow an user to subscribe to updates of the service.

Technologies used:

- Python
- FastAPI
- Twilio
- Rasa
- MongoDB
- Docker
- Docker Compose

# (total hours 15h)
## Use Case overview

User obtains a token to access to our API

User subscribes to updates of the service using the API, sending the token and a valid phone number.

Server sends a confirmation message to the requested phone number, to validate that the user wants to receive updates from the service.

User confirms to receive updates by sms

Server sends an update after 15s and other after 35s

User unsubscribes

Server sends a confirmation message
## API routes

The API has 3 routes:

- POST /login - Returns a JWT token for interacting with the API.
- GET /me - Returns the information about the token.
- GET /run - Initiates a sms conversation with the phone number sent.

For more documentation, read the OpenAPI spec at http://localhost:8080/docs

## Start the API

To start the API you need to execute the following command:
`make`

That will build the docker images needed by executing docker-compose build and start the API container at the port `8080`

The build process takes around 3-5 minutes, as it needs to download all the required software.

After that, the containers are going to start, but the API will wait 50s to let Rasa initialize.

The api will be located at `http://localhost:8080`
The default username is `spicy`
The default password is `soup`

## Clean environment

To remove the container and images of this API, run the following commands:  

`make stop`

`make clean`

## Project structure

Files related to application logic are inside the ``backend/app`` directory.
Application parts are:

```txt
api
├── auth                    - auth related deps and routes.
│   ├── deps                - dependencies for routes with auth.
│   └── auth                - auth related routes.
├── core                    - internal API objects.
│   ├── config.py           - settings for this api.
│   ├── database.py         - mongodb client and utils.
│   ├── message_handler.py  - in memory db .
│   ├── database.py         - in memory db .
│   ├── rasa_adapter.py     - settings for this api.
│   └── twilio_adapter.py   - settings for this api.
├── routes                  - web routes
│   └── subscriptions.py    - files related routes.
├── schemas                 - pydantic models for this api.
├── tests                   - unit tests for this api.
├── main.py                 - FastAPI application creation.
└── pre_start.py            - FastAPI application creation.
```

Files related to the conversational AI are inside the ``rasa`` directory.

## TODO

- Implement logging system and connect it with external providers like Sentry