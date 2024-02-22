# Ansible Fog Project Integration

## Description
<!-- Brief description of the project. -->

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