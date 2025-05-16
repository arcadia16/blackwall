import json


def check_data(data):
    print('\n', data, type(data))
    if isinstance(data, bytes):
        try:
            data = data.decode()
            parsed_json = json.loads(data)
            print("JSON parsed successfully", parsed_json)
            result = parsed_json
        except json.JSONDecodeError as err:
            print("JSONDecoder:", err)
            result = data
        except UnicodeDecodeError as err:
            print("Decoding:", err, data)
            result = data
        print(type(result))
        return result
    if data is None:
        data = str(None)
    print(type(data))
    return data


def fix_json(data: dict) -> dict:
    for key in data.keys():
        print(data[key], type(data[key]))
        data[key] = check_data(data[key])
    return data
