from parser_ozon import parser_ozon

# parser = parser_ozon.Parser_ozon('3D принтер')
# parser.parser()
# print(parser.result_parsing)

chat_id = '12345678'
user_request = '3D принтер'

result = parser_ozon.start_parser(chat_id, user_request)

print('Processing...')

print(result)
