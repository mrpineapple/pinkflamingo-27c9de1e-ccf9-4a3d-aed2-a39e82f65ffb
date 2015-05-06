# encoding: utf-8
# Created by Jeremy Bowman on Wed Dec  3 12:36:27 EST 2014
# Copyright (c) 2014 Safari Books Online, LLC. All rights reserved.

"""Default settings for logging information from Python code"""

from __future__ import unicode_literals

import os


def make_format(attributes):
    """Logging format string construction utility"""
    return '; '.join('{}: %({})s'.format(a, a) for a in attributes)

# Sets of logger attributes for use with make_format()
db_logger_attributes = ['duration']
request_logger_attributes = []  # ['status_code', 'request']
standard_logger_attributes = ['levelname', 'name', 'module', 'pathname', 'funcName', 'lineno', 'message']

LOG_JSON = 0
LOG_NAME = 'pinkflamingo.log'
LOG_POST = 0
SYSLOG_FACILITY = 'user'
SYSLOG_SOCKET = '/dev/log' if os.path.exists('/dev/log') else '/var/run/syslog'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'syslog': {
            'format': 'PINKFLAMINGO-MAIN ' + make_format(standard_logger_attributes),
        },
        'syslog-db': {
            'format': 'PINKFLAMINGO-MAIN ' + make_format(standard_logger_attributes + db_logger_attributes),
        },
        'syslog-request': {
            'format': 'PINKFLAMINGO-MAIN ' + make_format(standard_logger_attributes + request_logger_attributes),
        },
        'syslog-security': {
            'format': 'PINKFLAMINGO-SECURITY ' + make_format(standard_logger_attributes),
        },
        'simple': {
            'format': '[%(levelname)s] [%(asctime)s] [%(name)s]: %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'long_query': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': lambda record: record.duration > 0.05  # output slow queries only
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'syslog': {
            'level': 'DEBUG',
            'formatter': 'syslog',
            'class': 'logging.handlers.SysLogHandler',
            'address': SYSLOG_SOCKET,
            'facility': SYSLOG_FACILITY,
        },
        'syslog-db': {
            'level': 'DEBUG',
            'filters': ['long_query'],
            'formatter': 'syslog-db',
            'class': 'logging.handlers.SysLogHandler',
            'address': SYSLOG_SOCKET,
            'facility': SYSLOG_FACILITY,
        },
        'syslog-request': {
            'level': 'DEBUG',
            'formatter': 'syslog-request',
            'class': 'logging.handlers.SysLogHandler',
            'address': SYSLOG_SOCKET,
            'facility': SYSLOG_FACILITY,
        },
        'syslog-security': {
            'level': 'DEBUG',
            'formatter': 'syslog-security',
            'class': 'logging.handlers.SysLogHandler',
            'address': SYSLOG_SOCKET,
            'facility': SYSLOG_FACILITY,
        },
    },
    'loggers': {
        '': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'syslog-request'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends.*': {
            'handlers': ['mail_admins', 'syslog-db'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.security.DisallowedHost': {
            'handlers': ['syslog-security'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'nose': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'INFO',
            'propagate': False,
        },
        'requests': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'WARNING',
            'propagate': True,
        },
        'template_timings_panel': {
            'handlers': ['mail_admins', 'syslog'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}

