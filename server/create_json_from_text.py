import random

def create_json_from_text(text: str) -> dict:
    out = {}
    text_list = text.split()
    for i, item in enumerate(text_list):
        new_id = random.randint(0, len(text_list) - 1)
        while str(new_id) in out:
            new_id = random.randint(0, len(text_list) - 1)
        new_item = {'id': new_id, 'index': i, 'text':item}
        out[str(new_id)] = new_item
    return out


print(create_json_from_text(open('raw_lorem_ipsum.txt', 'r').read()))