#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import requests
import json
import logging
import collections

def make_request(
        method: str,
        url: str,
        fog_api_token: str,
        fog_user_token: str,
        payload: dict = None,
        timeout: int = 10
        ) -> (dict[str, str]):
    #url = url.rstrip("/")  # Ensure the URL ends with a single forward slash
    headers = {
        'fog-user-token': fog_user_token,
        'fog-api-token': fog_api_token,
        'Content-Type': 'application/json'  # Assuming JSON payload
    }

    try:
        response = requests.request(method, url, headers=headers, json=payload, timeout=timeout)
        response.raise_for_status()

        if response.text == 'success\n':
            response_json = {"status": "success"}
            return response_json
        try:
            response_json = response.json()
            if str(response_json) == "" or response_json == None or response_json == "null" or response_json == "None" or response_json == "none" or response_json == "NULL":
                response_json = {"status": "success"}
            return response_json
        except:
            response_json = {"status": "success"}
            return response_json
        
    except requests.exceptions.Timeout:
        logging.error(f"Request to {url} timed out after {timeout} seconds.")
        raise

    except requests.exceptions.RequestException as e:
        logging.error(f"Error while making request to {url}: {e}")
        raise

    except ValueError as ve:
        logging.error(ve)
        raise

def test_api_connection(
        url: str,
        fog_api_token: str,
        fog_user_token: str,
        timeout: int
        )-> (dict[str, str]):
    url = url.rstrip("/") + "/system/status"
    return make_request("GET", url, fog_api_token, fog_user_token, timeout)

def _get_hosts(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str,
        timeout: int
        ):
    url = f"{url}/host"
    return make_request("GET", url, fog_api_token, fog_user_token, timeout)

def _get_groups(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str,
        timeout
        ):
    url = f"{url}/group"
    return make_request("GET", url, fog_api_token, fog_user_token, timeout)

def list_hosts(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str, 
        output,
        timeout
        ):
    
    hosts_list = _get_hosts(url, fog_api_token, fog_user_token, timeout)
    hosts_fancy_list = {}
    hosts_fancy_list["Connection successful, hosts count:"] = {hosts_list["count"]}
    hosts_fancy_list["Output type"] = f"{output}"

    if output == 'minimal' or output is None:
        return hosts_fancy_list
    
    elif output == 'full':
        hosts_fancy_list["hosts"] = {}
        for host in hosts_list["hosts"]:
            for i in range(int(hosts_list["count"])+50):
                if int(host['id']) is i:
                    hosts_fancy_list['hosts'][i] = f"{host['description']}, {host['ip']}, {host['primac']}"
                else:
                    pass
        return hosts_fancy_list
    else:
        logging.error(f"Unknown output type '{output}'")
        raise
    
def list_groups(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str, 
        output,
        timeout: int = 10
        ):
    group_list = _get_groups(url, fog_api_token, fog_user_token, timeout)
    group_fancy_list = {}
    group_fancy_list["Connection successful, groups count:"] = {group_list["count"]}
    group_fancy_list["Output type"] = f"{output}"

    if output == 'minimal' or output is None:
        return group_fancy_list
    
    elif output == 'full':
        group_fancy_list["hosts"] = {}
        for group in group_list["groups"]:
            for i in range(int(group_list["count"])+50):
                if int(group['id']) is i:
                    group_fancy_list['hosts'][i] = f"{group['name']}, {group['description']}, {group['hostcount']}"
                else:
                    pass
        return group_fancy_list
    else:
        logging.error(f"Unknown output type '{output}'")
        raise

def add_hosts_to_group(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str, 
        group_name: str,
        hosts: list[str] = None
        )-> (dict[str, str]):
    # Implement your logic here
    pass

def _get_group_id(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str, 
        group_name: str, 
        timeout: int
        ):
    
    group_list = _get_groups(url, fog_api_token, fog_user_token, timeout)

    for group in group_list["groups"]:
        if str(group['name']) == str(group_name):
            return group['id']
        else:
            pass
    
    raise ValueError(f"Group '{group_name}' not found")

def _get_host_id(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str, 
        host_name: str, 
        timeout: int
        ):
    
    hosts_list = _get_hosts(url, fog_api_token, fog_user_token, timeout)

    for host in hosts_list["groups"]:
        if str(host['name']) == str(host_name):
            return host['id']
        else:
            pass
    
    raise ValueError(f"Host '{host_name}' not found")

def create_group(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str, 
        group_name: str,
        timeout: int
        ) -> (dict[str, str]):
    url = f"{url}/group/create"
    payload = {"name": group_name, "description": "Group created by Ansible"}
    return make_request("POST", url, fog_api_token, fog_user_token, payload, timeout)

def delete_group(
        url: str, 
        fog_api_token: str, 
        fog_user_token: str, 
        group_name: str, 
        timeout
        ) -> dict:
    id = _get_group_id(url, fog_api_token, fog_user_token, group_name, timeout)
    url = f"{url}/group/{id}/delete"
    response = make_request("DELETE", url, fog_api_token, fog_user_token, None, timeout)
    
    try:
        if response["status"] == "success":
            return {"status": "success", "message": f"Group '{group_name}' with id '{id}' deleted"}
    except:
        return response

def create_task_group(
        url: str,
        fog_api_token: str,
        fog_user_token: str,
        task_name: str, 
        group_name: str, 
        task_type: str, 
        timeout: int
        ) -> (dict[str, str]):
    id = _get_group_id(url, fog_api_token, fog_user_token, group_name, timeout)
    url = f"{url}/group/{id}/task"
    if task_type == "multicast":
        taskTypeID = 8
    else:
        raise ValueError(f"Unknown or not yet implemented task type '{task_type}'")
    payload = {
    "taskTypeID": taskTypeID,
    "wol": 1,
    "name": task_name
    }
    return make_request("POST", url, fog_api_token, fog_user_token, payload, timeout)

def create_task_host(
        url: str,
        fog_api_token: str,
        fog_user_token: str,
        task_name: str,
        host_name: str,
        task_type: str,
        timeout: int
        ) -> (dict[str, str]):
    id = _get_host_id(url, fog_api_token, fog_user_token, host_name, timeout)
    url = f"{url}/host/{id}/task"
    if task_type == "multicast":
        taskTypeID = 8
    else:
        raise ValueError(f"Unknown or not yet implemented task type '{task_type}'")
    payload = {
    "taskTypeID": taskTypeID,
    "wol": 1,
    "name": task_name
    }
    return make_request("POST", url, fog_api_token, fog_user_token, payload, timeout)

def list_tasks(url, fog_api_token, fog_user_token):
    # Implement your logic here
    pass

def main():
    module_args = dict(
        url=dict(type='str', required=True),
        fog_api_token=dict(type='str', required=True),
        fog_user_token=dict(type='str', required=True),
        action=dict(type='str', required=True),
        output=dict(type='str', required=False),
        group_name=dict(type='str', required=False),
        timeout=dict(type='int', required=False, default=10),
        host_name=dict(type='str', required=False),
        # Add other required parameters for specific actions
    )

    result = dict(
        changed=False,
        # Add other result fields as needed
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # Extract parameters
    url = module.params['url']
    fog_api_token = module.params['fog_api_token']
    fog_user_token = module.params['fog_user_token']
    action = module.params['action']
    output = module.params['output']
    if output is not type(str):
        output = "minimal"
    group_name = module.params['group_name']
    timeout = module.params['timeout']
    if timeout is None or timeout == '' or timeout == "null":
        timeout = 10
    host_name = module.params['host_name']

    # Implement logic based on the specified action
    if action == 'test_api_connection':
        result['test_connection'] = test_api_connection(url, fog_api_token, fog_user_token, timeout)
    elif action == 'list_hosts':
        result['hosts'] = list_hosts(url, fog_api_token, fog_user_token, output, timeout)
    elif action == 'list_groups':
        result['groups'] = list_groups(url, fog_api_token, fog_user_token, output, timeout)
    elif action == 'create_group':
        result['group'] = create_group(url, fog_api_token, fog_user_token, group_name, timeout)
    elif action == 'delete_group':
        result['group'] = delete_group(url, fog_api_token, fog_user_token, group_name, timeout)
    elif action == 'create_task_group':
        result['task'] = create_task_group(url, fog_api_token, fog_user_token, group_name, timeout)
    elif action == 'create_task_host':
        result['task'] = create_task_host(url, fog_api_token, fog_user_token, host_name, timeout)
    # Add other action cases...
    else:
        module.fail_json(f"Unknown action '{action}'")
        
    module.exit_json(**result)

if __name__ == '__main__':
    main()