# -*- coding: utf-8 -*-

"""Console script for gitlab_migration."""
import os
import sys

import click

from gitlab_migration import gitlab_migration as glm

@click.group()
def cli():
    pass

@cli.group()
def projects():
    """Commands for migrating projects."""
    return 0

@projects.command()
@click.argument('csv', type=click.File('r'))
@click.argument('target_base_url', type=click.STRING)
@click.argument('target_token', type=click.STRING)
def from_csv(csv, target_base_url, target_token):
    '''
    read in repos to action from a csv, migrate to target_base_url

    csv must contain two columns: source url in the first, and target base url in the second.
    target base url MUST be fleshed out. eg: `https://gitlab.example.com/` or `git@gitlab.example.com:`
    target_token must be an API-level private token valid on the target server
    '''
    for line in csv.readlines():
        old_url, target_group = [string.strip() for string in line.split(',')]
        click.echo(f"working on {old_url}...")
        glm.migrate_repo(old_url, target_base_url, target_group, target_token)

@projects.command()
@click.argument('csv', type=click.File('w'))
@click.argument('gitlab_url', type=click.STRING)
@click.argument('token', type=click.STRING)
def to_csv(csv, gitlab_url, token):
    '''
    get the SSH url for all projects (except archived projects) and write them to a (single-column) csv.

    WARNING: this will silently overwrite the specified file if it already exists
    '''
    click.echo(f"Fetching all project SSH URLs from {gitlab_url}...")
    csv.writelines([f"{url},\n" for url in glm.get_project_urls(gitlab_url, token)])
    click.echo("Done.")

@projects.command()
@click.argument('path', type=click.STRING)
@click.argument('new_base_url', type=click.STRING)
@click.argument('old_base_url', type=click.STRING)
@click.argument('target_group', type=click.STRING)
@click.option('set_as_origin', '--set-as-origin/--set-as-new', default=True)
def update_local(path, new_base_url, old_base_url, target_group, set_as_origin):
    for child_path in os.listdir(path):
        if os.path.isdir(child_path) and os.path.isdir(f"{child_path}/.git"):
            glm.update_local_repo(child_path, old_base_url, new_base_url, target_group, set_as_origin)


@cli.group()
def variables():
    """Commands for migrating group variables."""
    return 0


@variables.command()
@click.option('src_group', '--source-group', default=None, type=click.STRING, help="Leave blank to migrate vars from all groups")
@click.argument('target_group', type=click.STRING)
@click.argument('src_gitlab_url', type=click.STRING)
@click.argument('target_gitlab_url', type=click.STRING)
@click.argument('src_token', type=click.STRING)
@click.argument('target_token', type=click.STRING)
def migrate(src_group, target_group, src_gitlab_url, target_gitlab_url, src_token, target_token):
    '''
    migrate group variables from 1+ groups on one host to a single group on another host
    '''
    if src_group:
        src_group_id = glm._get_namespace_id(src_gitlab_url, src_group, src_token)
    else: 
        src_group_id = None

    target_group_id = glm._get_namespace_id(target_gitlab_url, target_group, target_token)

    for var in glm.get_group_vars(src_gitlab_url, src_token, src_group_id):
        glm.create_group_var(target_gitlab_url, target_token, var, target_group_id)


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover