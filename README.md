# Software Engineering

## app.py
This runs on the main server.
- `/api/v1/` is empty and a placeholder.
- `/api/v1/coins` returns the coins in JSON format.

## custom_logger
`custom_logger` is a wrapper for the Grafana Loki logging library that vastly simplifies the logging process and reduces it to a single line, as we do not need to make our configuration flexible at all.

### Example Code
```py
from custom_logger import Logger

self.logTitle = 'core'
self.logger = Logger()
self.logger.debugLog(self.logTitle, 'Example Debug')
self.logger.errorLog(self.logTitle, 'Example Error')
```

## colony_client
`colony_client` contains all of the code that runs on the user's computer when they need to initialise a colony.`

## sentiment_controller
`sentiment_controller` runs on the server and interacts with `app.py`.
