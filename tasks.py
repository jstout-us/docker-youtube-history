from pathlib import Path

from invoke import Collection
from invoke import task
from invoke.exceptions import Failure


@task
def scm_init(ctx):
    """Init git repo (if required) and configure git flow.

    Raises:
        Failure: .gitignore does not exist

    Returns:
        None
    """
    if not Path('.gitignore').is_file():
        raise Failure('.gitignore does not exist')

    new_repo = not Path('.git').is_dir()

    if new_repo:
        uri_remote = 'git@github.com:{}/{}.git'.format(ctx.scm.repo_owner,
                                                       ctx.scm.repo_slug
                                                      )

        ctx.run('git init')
        ctx.run('git add .')
        ctx.run('git commit -m "Initialize repo"')
        ctx.run('git remote add origin {}'.format(uri_remote))
        ctx.run('git tag -a "v_0.0.0" -m "cookiecutter ref"')

    ctx.run('git flow init -d')
    ctx.run('git flow config set versiontagprefix {}'.format(ctx.scm.version_tag_prefix))

    if new_repo:
        ctx.run('git push -u origin master')
        ctx.run('git push -u origin develop')
        ctx.run('git push --tags')


@task
def scm_push(ctx):
    """Push all branches and tags to origin."""

    for branch in ('develop', 'master'):
        ctx.run('git push origin {}'.format(branch))

    ctx.run('git push --tags')


@task
def scm_status(ctx):
    """Show status of remote branches."""
    ctx.run('git for-each-ref --format="%(refname:short) %(upstream:track)" refs/heads')


@task
def clean(ctx):
    """Clean Python bytecode."""
    ctx.run('find . | grep __pycache__ | xargs rm -rf')
    ctx.run('find . | grep .pytest_cache | xargs rm -rf')


@task(clean)
def build(ctx):
    """Build sdist and wheel."""
    ctx.run('docker build -t {} src'.format(ctx.docker.name))


@task(build)
def run(ctx):
    """Run container."""
    ctx.run('docker run -it {}'.format(ctx.docker.name), pty=True)


scm = Collection()
scm.add_task(scm_init, name="init")
scm.add_task(scm_push, name="push")
scm.add_task(scm_status, name="status")

ns = Collection(build, clean, run)
ns.add_collection(scm, name="scm")
