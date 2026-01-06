
LOG_DIR= "./logs"


#Logging configuration
LOG_CONFIG={
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - [%(levelname)s] %(name)s [%(module)s.%(funcName)s:%(lineno)d]: %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/server.log'.format(LOG_DIR),
            'maxBytes': 5000000,
            'formatter': 'standard',
            'backupCount': 2
        },
        'test': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '{}/testing.log'.format(LOG_DIR),
            'maxBytes': 5000000,
            'formatter': 'standard',
            'backupCount': 1
        },
    },
    'loggers': {
        '__main__': {
            'handlers': ['console', 'test'],
            'level': 'DEBUG',
            'propagate': False,
        },       
        'server': {
            'level': 'DEBUG',
            'handlers': ['file', 'console'],
            'propagate': False,
        },
        'location_to_gpx' : {
            'level': 'DEBUG'
        }
    },
    'root': {
        'level': 'ERROR',
        'handlers': ['file']
    }
}