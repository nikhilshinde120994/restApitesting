from api_helper import *
import uuid


class Test_Api:
    def test_can_create_item(self):
        # Create new Task
        user_id = f"user_id{uuid.uuid4().hex}"
        content = f"content{uuid.uuid4().hex}"
        payload = create_new_payload(content, user_id)
        create_task_response = create_new_task(payload)
        assert create_task_response.status_code == 200
        data = create_task_response.json()
        # Get task and validate it
        task_id = data['task']['task_id']
        get_task_response = get_task(task_id)
        assert get_task_response.status_code == 200
        get_task_data = get_task_response.json()
        validate_content(get_task_data, payload)

    def test_can_update_item(self):
        # Create new Task
        user_id = f"user_id{uuid.uuid4().hex}"
        content = f"content{uuid.uuid4().hex}"
        payload = create_new_payload(content, user_id)
        create_task_response = create_new_task(payload)
        assert create_task_response.status_code == 200
        data = create_task_response.json()
        # Update that task
        task_id = data['task']['task_id']
        updated_payload = {
            "content": "Updated string",
            "is_done": True,
            "task_id": task_id,
        }
        update_task_response = update_task(updated_payload)
        assert update_task_response.status_code == 200
        # Get task and validate it
        get_task_response = get_task(task_id)
        assert get_task_response.status_code == 200
        get_task_data = get_task_response.json()
        validate_content(get_task_data, updated_payload)

    def test_can_get_list_items(self):
        # Create new n numbers of tasks
        n = 3
        user_id = f"user_id{uuid.uuid4().hex}"

        for i in range(3):
            content = f"content{uuid.uuid4().hex}"
            payload = create_new_payload(content, user_id)
            create_task_response = create_new_task(payload)
            assert create_task_response.status_code == 200
        # Get list of task and check length
        list_task_response = list_task(user_id)
        assert list_task_response.status_code == 200
        assert len(list_task_response.json()['tasks']) == n

    def test_can_delete_item(self):
        # Create new Task
        user_id = f"user_id{uuid.uuid4().hex}"
        content = f"content{uuid.uuid4().hex}"
        payload = create_new_payload(content, user_id)
        create_task_response = create_new_task(payload)
        assert create_task_response.status_code == 200
        data = create_task_response.json()
        # Update that task
        task_id = data['task']['task_id']
        delete_task_response = delete_task(task_id)
        assert delete_task_response.status_code == 200
        # Get task and check that it is not found
        get_task_response = get_task(task_id)
        assert get_task_response.status_code == 404


