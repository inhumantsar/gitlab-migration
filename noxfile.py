from os.path import abspath
import os
import sys
import webbrowser

import nox

try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url


def _browser(path):
  webbrowser.open("file://" + pathname2url(abspath(path)))


@nox.session(reuse_venv=True, python=['3.6', '3.7'])
def test(session):
  """Runs pytest"""
  with open('requirements_dev.txt', 'r') as reqs_file:
    reqs = reqs_file.readlines()
  session.install(*reqs)
  session.run('pip', 'list')
  session.run('pytest')


@nox.session(reuse_venv=True)
def check_coverage(session):
  """Checks tests for total coverage. Outputs to stdout and htmlcov/"""
  with open('requirements_dev.txt', 'r') as reqs_file:
    reqs = reqs_file.readlines()
  session.install(*reqs)

  for cmd in [
        ['coverage', 'run', '--source', 'gitlab_migration', '-m', 'pytest'],
        ['coverage', 'report', '-m'],
        ['coverage', 'html']
      ]:
	  session.run(*cmd)
  _browser('htmlcov/index.html')


@nox.session(reuse_venv=True)
def lint(session):
  """Checks the project with pylint"""
  session.install('pylint')
  session.run('pylint')


@nox.session(reuse_venv=True)
def build_docs(session):
  """Builds documentation using Sphinx. Outputs to docs/, will open browser."""
  session.install('Sphinx')

  # clean up a bit first
  for del_file in ['docs/gitlab_migration.rst',
	                 'docs/modules.rst']:
    try:
      os.remove(del_file)
    except FileNotFoundError as fnfe: 
      pass
  
  # build docs
  session.run('sphinx-apidoc', '-o', 'docs/', 'gitlab_migration')
  # TODO: upload to S3? readthedocs? github pages?
  _browser('docs/')


@nox.session(reuse_venv=True)
def build_sdist(session):
  """Builds Source Distribution package. Outputs to dist/"""
  session.run('python3', 'setup.py', 'sdist')
  assert os.path.exists('dist/')