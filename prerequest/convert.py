import json
from .request_obj import RequestObject, EnumRequestType

def iter_folder(items: list, name: str):
    result_list = []

    for item in items:
        if "item" in item:
            result_list.append(iter_folder(item["item"], item["name"]))
        else:
            name = item.get("name", "New Request")

            request_args = item.get("request", {})
            method = request_args.get("method")
            headers = request_args.get("header")
            body = request_args.get("body")
            if body:
                body_type = body.get("mode")
                if body_type.startswith('form'):
                    body_type = EnumRequestType.MULTIPART
                    files = body.get("formdata", [])
                    payload = {}
                else:
                    body_type = EnumRequestType.APPLICATION
                    payload = json.loads(body.get("raw", {}))
                    files = None
            else:
                payload = {}
                files = None
                body_type = EnumRequestType.APPLICATION
            
            url = item.get("url", {}).get("raw", "")


            new_request = RequestObject(
                name=name,
                url=url,
                method=method,
                headers=headers,
                payload=payload,
                files=files,
                body_type=body_type
            )
            result_list.append(new_request)
    
    return result_list

def postman_to_obj(postman_json: str) -> list:
    try:
        json_loaded = json.load(open(postman_json, 'r'))
    except:
        raise Exception(f'file "{postman_to_obj}" is not a valid Json!')

    # Postman have two types of itens: Folders and Requests
    default_folder = json_loaded.get('item', [])
    default_info = json_loaded.get("info", {})
    default_name = default_info.get("name", "Collection")
    items = iter_folder(default_folder, default_name)
            
    return items