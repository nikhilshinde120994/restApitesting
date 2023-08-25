import requests


ENDPOINT = "https://todo.pixegami.io"


def create_new_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)


def create_new_payload(content, user_id):
    return {
      "content": content,
      "user_id": user_id,
      "is_done": False
    }


def update_task(payload):
    return requests.put(ENDPOINT + "/update-task/", json=payload)


def list_task(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def validate_content(data, payload):
    assert data['is_done'] == payload['is_done']
    assert data['content'] == payload['content']


def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")
