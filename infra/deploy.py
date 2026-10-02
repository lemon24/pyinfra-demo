from pyinfra import host
from pyinfra import local
from pyinfra.operations import apt
from pyinfra.operations import files
from pyinfra.operations import server

apt.update(name="apt update", cache_time=24 * 3600)

apt.packages(['nginx', 'python3-certbot-nginx'], name="install nginx")

disable_default = files.link(
    name="disable default site",
    path='/etc/nginx/sites-enabled/default',
    present=False,
)
server.service(
    name="reload nginx",
    service='nginx',
    reloaded=True,
    _if=disable_default.did_change,
)

if host.data.get('home_domain'):
    local.include('tasks/home.py')
if host.data.get('app_domain'):
    local.include('tasks/app.py')
