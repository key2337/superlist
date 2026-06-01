from fabric import task
import os

REPO_URL = 'git@github.com:key2337/superlist.git'
SITENAME = '39.105.88.230'

def _create_directory_structure_if_necessary(c):
    site_folder = f'/home/yyy/sites/{SITENAME}'
    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        c.run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(c):
    source_folder = f'/home/yyy/sites/{SITENAME}/source'
    if c.run(f'test -d {source_folder}/.git', warn=True).ok:
        c.run(f'cd {source_folder} && git fetch')
    else:
        c.run(f'git clone {REPO_URL} {source_folder}')
    current_commit = c.local('git log -n 1 --format=%H').stdout.strip()
    c.run(f'cd {source_folder} && git reset --hard {current_commit}')

def _update_settings(c):
    source_folder = f'/home/yyy/sites/{SITENAME}/source'
    settings_path = f'{source_folder}/notes/settings.py'
    c.run(f"sed -i 's/DEBUG = True/DEBUG = False/' {settings_path}")
    c.run(f"sed -i \"s/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = ['{SITENAME}', 'localhost']/\" {settings_path}")

def _update_virtualenv(c):
    source_folder = f'/home/yyy/sites/{SITENAME}/source'
    virtualenv_folder = f'{source_folder}/../virtualenv'
    if not c.run(f'test -f {virtualenv_folder}/bin/pip', warn=True).ok:
        c.run(f'python3 -m venv {virtualenv_folder}')
    c.run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(c):
    source_folder = f'/home/yyy/sites/{SITENAME}/source'
    c.run(f'cd {source_folder} && ../virtualenv/bin/python manage.py collectstatic --noinput')

def _update_database(c):
    source_folder = f'/home/yyy/sites/{SITENAME}/source'
    c.run(f'cd {source_folder} && ../virtualenv/bin/python manage.py migrate --noinput')

def _update_nginx_config(c):
    source_folder = f'/home/yyy/sites/{SITENAME}/source'
    c.put('deploy_tools/nginx.template.conf', '/tmp/nginx.template.conf')
    c.run(f"sed 's/SITENAME/{SITENAME}/g' /tmp/nginx.template.conf | sudo tee /etc/nginx/sites-available/{SITENAME}")
    c.run(f'sudo ln -sf /etc/nginx/sites-available/{SITENAME} /etc/nginx/sites-enabled/{SITENAME}')
    c.run('sudo systemctl reload nginx')

def _update_systemd_config(c):
    c.put('deploy_tools/gunicorn-systemd.template.service', '/tmp/gunicorn-systemd.template.service')
    c.run(f"sed 's/SITENAME/{SITENAME}/g' /tmp/gunicorn-systemd.template.service | sudo tee /etc/systemd/system/gunicorn-{SITENAME}.service")
    c.run('sudo systemctl daemon-reload')
    c.run(f'sudo systemctl enable gunicorn-{SITENAME}')
    c.run(f'sudo systemctl restart gunicorn-{SITENAME}')

@task
def deploy(c):
    _create_directory_structure_if_necessary(c)
    _get_latest_source(c)
    _update_settings(c)
    _update_virtualenv(c)
    _update_static_files(c)
    _update_database(c)
    _update_nginx_config(c)
    _update_systemd_config(c)
