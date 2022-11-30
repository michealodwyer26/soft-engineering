# Software Engineering

Disclaimer:
We are aware that there are hardcoded credentials in the repository. These have been rotated and **do not work**. Have a nice day.

## custom_logger
`custom_logger` is a wrapper for the Grafana Loki logging library that vastly simplifies the logging process and reduces it to a single line, as we do not need to make our configuration flexible at all.

### Example Code

```py
from cryptocolony.custom_logger import Logger

self.logTitle = 'core'
self.logger = Logger()
self.logger.debugLog(self.logTitle, 'Example Debug')
self.logger.errorLog(self.logTitle, 'Example Error')
```

## colony_client
`colony_client` contains all of the code that runs on the user's computer when they need to initialise a colony.`

## sentiment_controller
`sentiment_controller` runs on the server and interacts with `app.py`.

# API

This section will describe the REST API that interacts with the sentiment controller.
### API Title
```
GET /api/v1 HTTP/1.1
Host: 65.108.214.180
```
Returns a placeholder message for the API route.

### Create Colony
```
POST /api/v1/colony/create HTTP/1.1
Host: 65.108.214.180
Content-Type:application/json

{"name":"firstcolony"}
```

- The `name` parameter specifies an alphanumeric identifier for a colony.

### Create Bot
```
POST /api/v1/bot/create HTTP/1.1
Host: 65.108.214.180
Content-Type:application/json

{"colony":"example",
"id":"1"}
```


- The `colony` parameter specifies an alphanumeric identifier for a colony.
- The `id` parameter specifies the identifier of the bot that will be created.

### Get Colony
```
GET /api/v1/colony/<colony> HTTP/1.1
Host: 65.108.214.180
```
- Fetches a list of bots currently associated with a given `colony`.

### Get Bot
```
GET /api/v1/colony/<colony name>/<bot name> HTTP/1.1
Host: 65.108.214.180
```
- Fetches the details of a specified `bot` for a specified `colony`.
