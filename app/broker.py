from faststream.rabbit import RabbitBroker
from settings.settings import settings

broker = RabbitBroker(settings.broker_url)
