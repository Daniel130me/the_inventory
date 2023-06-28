import html
import re

def sanitize_data(data):
    if isinstance(data, str):
        #escape html content
        sanitized_data = html.escape(data)

        sanitized_data = sanitized_data.strip()

        return sanitized_data
    
    elif isinstance(data, list):
        sanitized_data = [sanitize_data(value) for value in data]
        return sanitized_data
    elif isinstance(data, dict):
        sanitized_data = {key: sanitize_data(value) for key,value in data.items()}
        return sanitized_data
    else:
        return data

def verify(model_class,value):
    print(value)
    print(model_class)
    result = model_class.objects.filter(email=value)
    # print(model_email)
    if not result:
        print('kjh')
        return False
    else:
        print('iop')
        return True