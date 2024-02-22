# Ansible Fog Project Integration

## Description
<!-- Brief description of the project. -->

The Ansible Fog Project Integration is a set of Ansible modules designed to streamline the interaction with a Fog Project server using its API. This integration allows users to perform various tasks, such as testing the API connection, listing hosts and groups, and executing specific actions on the Fog Project server.

### Features

- **Test API Connection:** Verify the connectivity to the Fog Project server's API using provided authentication tokens.
  
- **List Hosts and Groups:** Retrieve information about hosts and groups from the Fog Project server, providing options for minimal or detailed output.

- **Flexible Usage:** Execute Ansible playbooks with specific actions to interact with the Fog Project server based on your requirements.

Follow the provided instructions to clone the repository, navigate to the project directory, install dependencies, and execute Ansible modules. Use the usage examples to integrate the Ansible modules into your workflow seamlessly.


## Getting Started
<!-- Instructions on how to get the project up and running. -->

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/ansible-fog-project.git
    ```

2. Navigate to the project directory:
    ```bash
    cd ansible-fog-project
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

4. Execute the Ansible modules:
    ```bash
    ansible-playbook your_playbook.yml
    ```

## Usage
<!-- Examples and instructions on how to use the Ansible modules. -->

### Test API Connection

```bash
ansible-playbook your_playbook.yml -e "action=test_api_connection url=https://your-fog-server/api fog_api_token=your-api-token fog_user_token=your-user-token"
```

### List Hosts (Minimal Output)

```bash
ansible-playbook your_playbook.yml -e "action=list_hosts url=https://your-fog-server/api fog_api_token=your-api-token fog_user_token=your-user-token output=minimal"
````

### List Hosts (Full Output)

```bash
ansible-playbook your_playbook.yml -e "action=list_hosts url=https://your-fog-server/api fog_api_token=your-api-token fog_user_token=your-user-token output=full"
```

### List Groups (Minimal Output)

```bash
ansible-playbook your_playbook.yml -e "action=list_groups url=https://your-fog-server/api fog_api_token=your-api-token fog_user_token=your-user-token output=minimal"
```

### List Groups (Full Output)

```bash
ansible-playbook your_playbook.yml -e "action=list_groups url=https://your-fog-server/api fog_api_token=your-api-token fog_user_token=your-user-token output=full"
```

## Contributing
<!-- Guidelines for contributing to the project. -->
1. Fork the repository.
2. Create a new branch for your feature: git checkout -b feature-name.
3. Commit your changes: git commit -m 'Add new feature'.
4. Push to the branch: git push origin feature-name.
5. Submit a pull request.

## License
<!-- Information about the project's license. -->
This project is licensed under the MIT License.