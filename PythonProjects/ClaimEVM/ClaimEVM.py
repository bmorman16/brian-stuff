import requests

# Replace these variables with your own
GITLAB_URL = 'https://git.web.boeing.com'  # or your GitLab instance URL
ACCESS_TOKEN = 'Zso1BU5ZFkyzBzuAC_ix'  # Your personal access token
PROJECT_ID = 129604# Your project ID

# Issue details
issue_title = 'Claim EVM'
issue_description = 'Weekly reminder to claim performance.'
labels = 'Now,Automation'  # Tag for the issue

# Create the issue
def create_issue():
    url = f'{GITLAB_URL}/api/v4/projects/{PROJECT_ID}/issues'
    headers = {
        'Private-Token': ACCESS_TOKEN
    }
    data = {
        'title': issue_title,
        'description': issue_description,
        'labels': labels
    }

    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 201:
        print('Issue created successfully:', response.json())
    else:
        print('Failed to create issue:', response.status_code, response.text)

if __name__ == '__main__':
    create_issue()
