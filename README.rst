==============================
GitLab -> GitLab API Migration
==============================

This one-off project migrates every project in one GitLab instance to another using the API and Git

GitLab's built in Import/Export wasn't suitable for this situation, and I wanted to gracefully merge 
everything into a single namespace.


* Free software: MIT license

* Documentation: https://gitlab-migration.readthedocs.io.


Projects
----------

1. `glm projects to_csv /path/to/csv https://gitlab.example.com/ Y0uRT0k3NH3re` will produce a single-column CSV with just the SSH clone URLs
2. Edit the CSV to include a target group name for each repo. eg: `git@gitlab.example.com:oldgroupname/somerepo.git,newgroupname`
3. `glm projects from_csv /path/to/csv git@newgitlab.example.com: N3WT0K3NH3R3` will loop through each line in the CSV and:
    1. Create a new repo on the new GitLab using the group specified and the repo name (extracted from current url)
    2. Clone the source repo to a tmp dir
    3. Add the new GitLab as a new remote
    4. Push the repo to the new remote

Group Variables
---------------

```
Usage: glm variables migrate [OPTIONS] TARGET_GROUP SRC_GITLAB_URL
                             TARGET_GITLAB_URL SRC_TOKEN TARGET_TOKEN

  migrate group variables from 1+ groups on one host to a single group on
  another host

Options:
  --source-group TEXT  Leave blank to migrate vars from all groups
  --help               Show this message and exit.
```


Credits
-------

This package was created with Cookiecutter_ and the `inhumantsar/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`inhumantsar/cookiecutter-pypackage`: https://github.com/inhumantsar/cookiecutter-pypackage
