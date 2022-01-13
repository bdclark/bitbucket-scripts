#!/usr/bin/env python

import json
import os
import requests


def get_repo_list(workspace, username, password, project_key=None, next_url=None):
    results = []
    url = f"https://api.bitbucket.org/2.0/repositories/{workspace}"
    headers = {"Accept": "application/json"}
    params = f'q=project.key="{project_key}"'
    if next_url is not None:
        url = next_url
        params = None
    response = requests.get(
        url, headers=headers, params=params, auth=(username, password)
    )
    data = response.json()
    for repo in data["values"]:
        https = [l["href"] for l in repo["links"]["clone"] if l["name"] == "https"][0]
        ssh = [l["href"] for l in repo["links"]["clone"] if l["name"] == "ssh"][0]
        results.append(
            {
                "uuid": repo["uuid"],
                "full_name": repo["full_name"],
                "name": repo["name"],
                "created_on": repo["created_on"],
                "updated_on": repo["updated_on"],
                "slug": repo["slug"],
                "description": repo["description"],
                "links": {
                    "self": repo["links"]["self"]["href"],
                    "https_clone": https,
                    "ssh_clone": ssh,
                },
                "project": {
                    "name": repo["project"]["name"],
                    "key": repo["project"]["key"],
                },
            }
        )
    if "next" in data:
        results = results + get_repo_list(
            workspace, username, password, project_key, data["next"]
        )
    return results



BITBUCKET_USERNAME = os.environ["BITBUCKET_USERNAME"]
BITBUCKET_PASSWORD = os.environ["BITBUCKET_PASSWORD"]

repos = get_repo_list("kinneygroup", BITBUCKET_USERNAME, BITBUCKET_PASSWORD, "AA")
print(json.dumps(repos[0], indent=2))
