
import json
import os
from github import Github

with open('results.json', 'r') as f:
    results = json.load(f)

g = Github(os.environ['GITHUB_TOKEN'])
repo = g.get_repo(os.environ['GITHUB_REPOSITORY'])

for browser in ['chrome', 'firefox']:
    for url, data in results[browser].items():
        if data['status'] == 'Missing Images':
            issue_title = f"Missing images on {url} ({browser})"
            issue_body = "The following images are missing:\n\n"
            for img in data['missing_images']:
                issue_body += f"- {img['name']} ({img['url']})\n"

            # Check if an open issue already exists
            existing_issues = repo.get_issues(state='open', labels=['missing-images'])
            issue_exists = any(issue.title == issue_title for issue in existing_issues)

            if not issue_exists:
                repo.create_issue(title=issue_title, body=issue_body, labels=['missing-images'])