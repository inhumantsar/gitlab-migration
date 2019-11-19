# -*- coding: utf-8 -*-

import os
import shutil
import re
import subprocess
import tempfile

from git import Repo
import requests

# disable ssl warnings. BAD PRACTICE.
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



"""Main module."""

def migrate_repo(url, target_base_url, target_group, token):
    '''
    this will clone a repo from one remote and push it to another. 
    
    target_base_url *must* include everything up to the group name. eg: `https://<url>/` or `git@<url>:`
    '''
    try:
        _create_repo(url, target_base_url, target_group, token)
    except Exception as e:
        print(f"CREATE REPO ERROR! SKIPPING! {e}")
        return

    tmpdir = tempfile.mkdtemp()
    repo = Repo.clone_from(url, tmpdir)
    new_remote = repo.create_remote('new', 
        url=_get_new_repo_url(url, target_base_url, target_group))

    try:
        print('Pushing...')
        new_remote.push()
    except Exception as e:
        print(f"PUSH ERROR! SKIPPING REPO! {e}")

    shutil.rmtree(tmpdir)


def update_local_repo(path, old_base_url, target_base_url, target_group, set_as_origin):
    '''
    this will update a local repo with a new origin, saving the old origin with the remote name "old"
    
    target_base_url *must* include everything up to the group name. eg: `https://<url>/` or `git@<url>:`
    '''
    repo = Repo(path)
    old_remote = repo.remotes.origin
    if old_base_url not in old_remote.url:
        print(f'SKIPPING: Old base URL not present in origin URL for {path}')
        return

    new_url = _get_new_repo_url(old_remote.url, target_base_url, target_group)
    if set_as_origin:
        if "old" in [r.name for r in repo.remotes]:
            print(f"SKIPPING: A remote named 'old' already exists for {_get_repo_name_from_url(old_remote.url)}")
        else:
            repo.create_remote("old", url=old_remote.url)
        repo.delete_remote(old_remote)
        repo.create_remote('origin', url=new_url)
    else:
        repo.create_remote('new', url=new_url)


def get_project_urls(gitlab_url, token):
    headers = {"Private-Token": token}
    project_urls = []
    page = 1
    while True:
        resp = requests.get(f"{gitlab_url}/api/v4/projects?archived=false&page={page}", headers=headers, verify=False)
        project_urls += [item['ssh_url_to_repo'] for item in resp.json()]
        if 'X-Next-Page' in resp.headers:
            if resp.headers['X-Next-Page'] == '':
                break
            page = resp.headers['X-Next-Page']
            # print(f"continuing to page {page}")

    return project_urls


def get_group_vars(gitlab_url, token, group_id=None):
    headers = {"Private-Token": token}
    group_ids = [group_id] if group_id else _get_group_ids(gitlab_url, token)
    variables = []
    for gid in group_ids:
        variables += requests.get(f"{gitlab_url}/api/v4/groups/{gid}/variables", headers=headers, verify=False).json()
    
    return variables

def create_group_var(gitlab_url, token, var, group_id):
    '''vars should be a dict containing at least two keys: "key" and "value".'''
    headers = {"Private-Token": token}
    resp = requests.post(f"{gitlab_url}/api/v4/groups/{group_id}/variables", headers=headers, data=var, verify=False)
    if resp.status_code > 299:
        print(f"ERROR: Variable {var['key']} not created. {resp.text}")


def _get_group_ids(gitlab_url, token):
    headers = {"Private-Token": token}
    group_ids = []
    page = 1
    while True:
        resp = requests.get(f"{gitlab_url}/api/v4/groups?all_available=true&page={page}", headers=headers, verify=False)
        group_ids += [item['id'] for item in resp.json()]
        if 'X-Next-Page' in resp.headers:
            if resp.headers['X-Next-Page'] == '':
                break
            page = resp.headers['X-Next-Page']
            # print(f"continuing to page {page}")

    return group_ids


def _get_repo_name_from_url(url):
    try:
        return re.match('.*\/([-_.a-zA-Z0-9]+)\.git$', url)[1]
    except:
        raise Exception(f"project name not found in url. bad url? {url}")


def _get_new_repo_url(old_url, target_base_url, target_group):
    if target_base_url.startswith('git@') and target_base_url[-1] != ':':
        target_base_url = f"{target_base_url}:" 
    if target_base_url.startswith('https://') and target_base_url[-1] != '/':
        target_base_url = f"{target_base_url}/" 
    return f"{target_base_url}{target_group}/{_get_repo_name_from_url(old_url)}.git"


def _create_repo(old_url, target_base_url, target_group, token):
    url = target_base_url
    if '@' in url:
        url = f"https://{url.split('@')[1]}/"
    namespace = _get_namespace_id(url, target_group, token)
    headers = {"Private-Token": token}
    data = {'name': _get_repo_name_from_url(old_url), 'namespace_id': namespace, 'visibility': 'internal'}
    print(f"Creating repo: {target_group}/{data['name']}...")
    resp = requests.post(f"{url}api/v4/projects", headers=headers, data=data, verify=False)
    if resp.status_code > 299:
        raise Exception(f"Unable to create repo: {resp.text}")
        

def _get_namespace_id(url, group_name, token):
    headers = {"Private-Token": token}
    resp = requests.get(f"{url}api/v4/namespaces?search={group_name}", headers=headers, verify=False)
    results = resp.json()
    # print(results)
    if len(results) > 1:
        raise Exception(f"Too many namespace results returned, group_name is ambiguous: {group_name}")
    return results[0]['id']
