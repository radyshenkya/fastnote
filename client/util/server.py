import requests
import json
from random import choices
from hashlib import md5


def generate_user_token() -> str:
    USER_TOKEN_ITERATIONS = 32
    GENERATION_ALPHABET = "abcdefghijklmnopqrst1234567890"
    return md5(
        ("".join(choices(GENERATION_ALPHABET, k=USER_TOKEN_ITERATIONS))).encode("utf-8")
    ).hexdigest()


def clear_address(address: str) -> str:
    if len(address) == 0:
        pass
    elif address[-1] == "/":
        return address[:-1]
    return address


def assert_status(original_status_code, needed_status_code):
    if original_status_code != needed_status_code:
        raise IOError(
            "Status Code is "
            + str(original_status_code)
            + ". Need "
            + str(needed_status_code)
        )


def ping_server(server_point: str) -> bool:
    res = requests.get(server_point)
    return res.status_code == 200


def get_random_token(server_point: str) -> str:
    res = requests.get(clear_address(server_point) + "/api/get_token")
    assert_status(res.status_code, 200)
    json_obj = json.loads(res.content)

    return json_obj["token"]


def get_user_note_ids(server_point: str, user_token: str):
    res = requests.get(f"{clear_address(server_point)}/api/{user_token}/note")
    assert_status(res.status_code, 200)
    json_obj = json.loads(res.content)

    return json_obj["ids"]


def new_note(server_point: str, user_token: str, text: str, is_private: bool):
    res = requests.post(
        f"{clear_address(server_point)}/api/{user_token}/note",
        json={"text": text, "is_private": is_private},
    )
    assert_status(res.status_code, 201)
    json_obj = json.loads(res.content)

    return json_obj["id"]


def is_owned_note(server_point: str, user_token, id: str) -> bool:
    res = requests.get(f"{clear_address(server_point)}/api/{user_token}/note")
    assert_status(res.status_code, 200)
    json_obj = json.loads(res.content)

    return id in json_obj["ids"]


def get_note_details(server_point: str, user_token: str, id: str):
    res = requests.get(
        f"{clear_address(server_point)}/api/{user_token}/note/{id}")
    assert_status(res.status_code, 200)

    json_obj = json.loads(res.content)

    return json_obj


def patch_note(
    server_point: str, user_token: str, id: str, text: str, is_private: bool
):
    res = requests.patch(
        f"{clear_address(server_point)}/api/{user_token}/note/{id}",
        json={"text": text, "is_private": is_private},
    )
    assert_status(res.status_code, 200)

    json_obj = json.loads(res.content)

    return json_obj["ok"]


def delete_note(server_point: str, user_token: str, id: str):
    res = requests.delete(
        f"{clear_address(server_point)}/api/{user_token}/note/{id}")
    assert_status(res.status_code, 200)

    json_obj = json.loads(res.content)

    return json_obj["ok"]
