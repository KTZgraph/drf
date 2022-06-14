import requests

product_id = input("What is the produt id you want to use")
try:
    product_id = int(product_id)
except:
    product_id = None
    print(f'{product_id} not a valid id')

if product_id:
    endpoint = f"http://localhost:8000/api/products/{product_id}/delete/"  #działa jednroazowo no bo usunięcie

    get_response = requests.delete(endpoint) # HTTP  Request 
    # print(get_response.json())
    # raise RequestsJSONDecodeError(e.msg, e.doc, e.pos)
    # requests.exceptions.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
    print(get_response.status_code, get_response.status_code == 204)


