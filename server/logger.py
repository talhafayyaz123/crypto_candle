import logging
import logging.config
import yaml

# Logging
with open('logging.yml', 'r') as f:
    CONFIG = yaml.safe_load(f)
    logging.config.dictConfig(CONFIG)

logger = logging.getLogger('app')
werk_logger = logging.getLogger('werkzeug')
