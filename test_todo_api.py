import requests
import uuid

ENDPOINT = 'https://todo.pixegami.io/'


def test_can_create_task():
    payload = new_task_payload()
    create_task_response = crete_new_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    response_time = create_task_response.elapsed.total_seconds()
    print(response_time)
    task_id = data['task']['task_id']
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == payload['content']
    assert get_task_data['user_id'] == payload['user_id']
    assert get_task_data['is_done'] == payload['is_done']


def test_can_update_task():
    # Create new task
    payload = new_task_payload()
    create_task_response = crete_new_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()['task']['task_id']
    # Update the task
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "My test content",
        "is_done": True,
    }
    updated_task_response = update_task(new_payload)
    assert updated_task_response.status_code == 200
    # Get and validate the changes
    get_task_response = get_task(task_id)
    get_task_data = get_task_response.json()
    assert get_task_data['content'] == new_payload['content']
    assert get_task_data['is_done'] == new_payload['is_done']


def test_can_list_tasks():
    # create N tasks
    n = 3
    payload = new_task_payload()
    for i in range(n):
        create_task_response = crete_new_task(payload)
        assert create_task_response.status_code == 200

    # List tasks, and check that there are n numbers of item
    user_id = payload['user_id']
    list_task_response = get_list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    tasks = data['tasks']
    assert len(tasks) == n


def test_can_delete_task():
    # Create new task
    payload = new_task_payload()
    create_task_response = crete_new_task(payload)
    assert create_task_response.status_code == 200
    # Delete the task
    task_id = create_task_response.json()['task']['task_id']
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200
    # Get the task, and check that it is not found
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def crete_new_task(payload):
    return requests.put(ENDPOINT + '/create-task', json=payload)


def update_task(payload):
    return requests.put(ENDPOINT + '/update-task', json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f'/get-task/{task_id}')


def delete_task(task_id):
    return requests.delete(ENDPOINT + f'/delete-task/{task_id}')


def get_list_tasks(user_id):
    return requests.get(ENDPOINT + f'/list-tasks/{user_id}')


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"content_{uuid.uuid4().hex}"
    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }
