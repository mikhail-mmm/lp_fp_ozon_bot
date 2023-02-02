# import dramatiq
# from dramatiq.brokers.rabbitmq import RabbitmqBroker
from parser_ozon.parser_ozon import Parser

# dramatiq.set_broker(RabbitmqBroker())

# @dramatiq.actor
def start_parser(chat_id, user_request):
    parser = Parser(chat_id, user_request)
    parser.parser_ozon()
    parser.seve_data()

if __name__ == '__main__':
    start_parser('123321', '3D принтер')