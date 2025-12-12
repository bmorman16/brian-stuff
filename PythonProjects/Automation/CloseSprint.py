import requests

# Replace these variables with your own
GITLAB_URL = 'https://git.web.boeing.com/api/v4'  # GitLab API URL
ACCESS_TOKEN = 'Zso1BU5ZFkyzBzuAC_ix'  # Your personal access token
PROJECT_ID = 129604  # Your project ID

def close_issues_with_label(label):
    page = 1
    while True:
        # Fetch all issues for the project with pagination
        response = requests.get(f"{GITLAB_URL}/projects/{PROJECT_ID}/issues?page={page}&per_page=100", 
                                headers={'Authorization': f'Bearer {ACCESS_TOKEN}'})
        
        if response.status_code != 200:
            print(f"Failed to fetch issues: {response.text}")
            return

        issues = response.json()
        
        if not issues:
            break  # Exit the loop if no more issues are found

        for issue in issues:
            print(f"Issue ID: {issue['iid']}, Labels: {issue.get('labels', [])}")  # Debugging line
            if label in issue.get('labels', []):
                issue_iid = issue['iid']  # Use the internal ID (IID) of the issue
                # Close the issue
                close_response = requests.put(f"{GITLAB_URL}/projects/{PROJECT_ID}/issues/{issue_iid}", 
                                               headers={'Authorization': f'Bearer {ACCESS_TOKEN}'},
                                               json={'state_event': 'close'})
                if close_response.status_code == 200:
                    print(f"Issue {issue_iid} closed successfully.")
                else:
                    print(f"Failed to close issue {issue_iid}: {close_response.text}")

        page += 1  # Move to the next page

# Call the function with the desired label
close_issues_with_label('Sprint Review')
