import platform

if platform.node() == 'Norida':
	DEBUG = True
else:
	DEBUG = False

if DEBUG:
	BROKER_BACKEND = "sqlakombu.transport.Transport"
	BROKER_HOST = "sqlite:////tmp/celerydb.sqlite"
	CELERY_RESULT_DBURI = "sqlite:////tmp/celerydb.sqlite"
else:
	BROKER_HOST = "rabbitmq.elpis.dotcloud.com"
	BROKER_PORT = 6216
	BROKER_USER = "root"
	BROKER_PASSWORD = "lV>RIWwuJm]]YqD!%WiI"
	CELERY_RESULT_BACKEND = "amqp"
