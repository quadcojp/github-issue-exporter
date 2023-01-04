import os
from os.path import join, dirname
from dotenv import load_dotenv
from github import Github
import pandas as pd


def main():
    dotenv_path = join(dirname(__file__), '.env')
    load_dotenv(dotenv_path)

    # repos = ['mc-map-app', 'mc-map-backend', 'mc-map-batch',
    #          'mcportal-app-ph2', 'mcportal-webapp-ph2', 'mcportal-backend-ph2', 'mcportal-batch',
    #          'yrb-app', 'yrb_admin-api', 'yrb-batch']
    repos = os.environ.get("REPOS").split(',')

    g = Github(os.environ.get("TOKEN"))

    issue_list = []

    for repo in repos:
        for issue in g.get_organization(os.environ.get("ORG")).get_repo(repo).get_issues(state="all"):
            if '/pull/' in issue.html_url:
                # issueとprが取得されるので、prだったらスキップ
                continue
            issue_list.append([repo, issue.title, issue.state, ",".join([l.name for l in issue.labels]), issue.html_url, issue.body])

    df = pd.DataFrame(issue_list, columns=['repository', 'title', 'status', 'labels', 'url', 'body'])
    df.to_excel('output/issues.xlsx')


if __name__ == '__main__':
    main()
