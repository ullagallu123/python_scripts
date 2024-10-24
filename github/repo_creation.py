import hvac
import requests

# Vault configuration
VAULT_URL = 'http://127.0.0.1:8200'  # Replace with your Vault server address
VAULT_TOKEN = input("Enter your Vault token: ").strip()

# GitHub configuration
GITHUB_USERNAME = 'your_github_username'
VAULT_SECRET_PATH = 'secret/github'

# Initialize Vault client
client = hvac.Client(url=VAULT_URL, token=VAULT_TOKEN)

# Read GitHub token from Vault
read_response = client.secrets.kv.v2.read_secret_version(path=VAULT_SECRET_PATH)
github_token = read_response['data']['data']['token']

# Repository details
repo_name = 'vault-integrated-repo'
description = 'Repository created using a GitHub token stored in HashiCorp Vault.'
private = False  # Set to True if you want the repository to be private

# GitHub API URL for creating a repository
url = 'https://api.github.com/user/repos'

# Request headers
headers = {
    'Authorization': f'token {github_token}',
    'Accept': 'application/vnd.github.v3+json'
}

# Request body
data = {
    'name': repo_name,
    'description': description,
    'private': private
}

# Make the request to create the repository
response = requests.post(url, headers=headers, json=data)

# Check the response
if response.status_code == 201:
    print(f'Successfully created repository: {repo_name}')
else:
    print(f'Failed to create repository: {response.status_code}')
    print(response.json())
