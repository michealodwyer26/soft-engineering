import logging
import logging_loki

class Logger:

    def __init__(self):
        self.logger = logging.getLogger("project-logger") 
        self.handler = logging_loki.LokiHandler(url="http://65.108.214.180:3100/loki/api/v1/push", version="1")
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)
        logging_loki.emitter.LokiEmitter.level_tag = "level"
        
    def debugLog(self, controller: str, message: str):
        self.logger.debug(message, extra={"tags": {"service": controller}})
    
    def errorLog(self, controller: str, message: str):
        self.logger.error(message, extra={"tags": {"service": controller}})
