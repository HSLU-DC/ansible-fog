#!/usr/bin/python
from ansible.module_utils.basic import AnsibleModule
import requests
import json
import logging
import collections

def test_api_connection(url, fog_api_token, fog_user_token, timeout=10):
    url = url.rstrip("/") + "/system/status"  # Ensure the URL ends with a single forward slash
    payload = {}
    headers = {
        'fog-user-token': fog_user_token,
        'fog-api-token': fog_api_token
    }

    try:
        response = requests.get(url, headers=headers, data=payload, timeout=timeout)
        if response.status_code == 200:
            return "Successful!"
        else:
            return "Unsuccessful!" 
        # Check for HTTP errors
        response.raise_for_status()

        # Check for API-level errors
        response_json = response.json()
        if response_json.get('error'):
            raise ValueError(f"Fog API error: {response_json['error']['message']}")

    except requests.exceptions.Timeout:
        logging.error(f"Request to {url} timed out after {timeout} seconds.")
        raise

    except requests.exceptions.RequestException as e:
        logging.error(f"Error while making request to {url}: {e}")
        raise

    except ValueError as ve:
        logging.error(ve)
        raise

def get_hosts(url, fog_api_token, fog_user_token, timeout=10):
    url = url.rstrip("/") + "/host"  # Ensure the URL ends with a single forward slash
    payload = {}
    headers = {
        'fog-user-token': fog_user_token,
        'fog-api-token': fog_api_token
    }

    try:
        response = requests.get(url, headers=headers, data=payload, timeout=timeout)

        # Check for HTTP errors
        response.raise_for_status()

        # Check for API-level errors
        response_json = response.json()
        if response_json.get('error'):
            raise ValueError(f"Fog API error: {response_json['error']['message']}")

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

def get_groups(url, fog_api_token, fog_user_token, timeout=10):
    url = url.rstrip("/") + "/group"  # Ensure the URL ends with a single forward slash
    payload = {}
    headers = {
        'fog-user-token': fog_user_token,
        'fog-api-token': fog_api_token
    }

    try:
        response = requests.get(url, headers=headers, data=payload, timeout=timeout)

        # Check for HTTP errors
        response.raise_for_status()

        # Check for API-level errors
        response_json = response.json()
        if response_json.get('error'):
            raise ValueError(f"Fog API error: {response_json['error']['message']}")

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

def list_hosts(url, fog_api_token, fog_user_token, output='minimal'):
    hosts_list = get_hosts(url, fog_api_token, fog_user_token)
    hosts_fancy_list = {}
    hosts_fancy_list["Connection successful, hosts count:"] = {hosts_list["count"]}
    hosts_fancy_list["Output type"] = f"{output}"

    if output == 'minimal':
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

def list_groups(url, fog_api_token, fog_user_token, output='minimal'):
    group_list = get_groups(url, fog_api_token, fog_user_token)
    group_fancy_list = {}
    group_fancy_list["Connection successful, hosts count:"] = {group_list["count"]}
    group_fancy_list["Output type"] = f"{output}"

    if output == 'minimal':
        return group_fancy_list
    
    elif output == 'full':
        group_fancy_list["hosts"] = {}
        for group in group_list["groups"]:
            for i in range(int(group_list["count"])+50):
                if int(group['id']) is i:
                    group_fancy_list['hosts'][i] = f'{group['name']}, {group['description']}, {group['hostcount']}'
                else:
                    pass
        return group_fancy_list
    else:
        logging.error(f"Unknown output type '{output}'")
        raise

def add_hosts_to_group(url, fog_api_token, fog_user_token, group_name, hosts):
    # Implement your logic here
    pass

def create_group(url, fog_api_token, fog_user_token, group_name):
    # Implement your logic here
    pass

def create_task(url, fog_api_token, fog_user_token, task_name, multicast_targets):
    # Implement your logic here
    pass

def list_tasks(url, fog_api_token, fog_user_token):
    # Implement your logic here
    pass

def main(linter=False):
    if linter:
        return
    module_args = dict(
        url=dict(type='str', required=True),
        fog_api_token=dict(type='str', required=True),
        fog_user_token=dict(type='str', required=True),
        action=dict(type='str', required=True),
        output=dict(type='str', required=False),
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

    # Implement logic based on the specified action
    if action == 'test_api_connection':
        result['test_connection'] = test_api_connection(url, fog_api_token, fog_user_token)
    elif action == 'list_hosts':
        result['hosts'] = list_hosts(url, fog_api_token, fog_user_token, output)
    elif action == 'list_groups':
        result['groups'] = list_groups(url, fog_api_token, fog_user_token, output)
    # Add other action cases...
    else:
        module.fail_json(f"Unknown action '{action}'")
        
    module.exit_json(**result)

if __name__ == '__main__':
    main(linter=True)
