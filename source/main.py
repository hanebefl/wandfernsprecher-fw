from logging import DEBUG, INFO, WARNING, ERROR, basicConfig as logConfig

LOG_LEVEL = DEBUG
logConfig(format="%(asctime)10s %(levelname)-8s %(message)s", level=LOG_LEVEL)

import phoneui
