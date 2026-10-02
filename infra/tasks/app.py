from pyinfra import host
from pyinfra.operations import apt
from pyinfra.operations import files
from pyinfra.operations import pip
from pyinfra.operations import server
from pyinfra.operations import systemd
from pyinfra.operations.util import any_changed

from modules import nginx

server.group('app', name="create app group")
server.group('app-socket', name="create socket group")
server.user(
    name="create user",
    user='app',
    group='app',
    groups=['app-socket'],
    home="/var/lib/app",
    shell="/usr/sbin/nologin",
    system=True,
)
server.user(
    name="nginx socket access",
    user='www-data',
    groups=['app-socket'],
    append=True,
)

apt.packages('python3-venv', name="install venv")
pip.venv('/opt/app', 'python3', name="create venv")
pip.packages(['gunicorn'], virtualenv='/opt/app', name="install deps")

sync_files = files.sync(
    name="sync app files",
    src='../app',
    dest='/opt/app/src',
    delete=True,
    exclude_dir=['**/__pycache__'],
)
install_app = server.shell(
    "/opt/app/bin/pip install /opt/app/src",
    name="install app",
    _if=sync_files.did_change,
)

write_service = files.template(
    name="write service",
    src='templates/systemd/app.service',
    dest='/etc/systemd/system/app.service',
)
systemd.service(
    name="enable service",
    service='app.service',
    enabled=True,
    restarted=True,
    daemon_reload=True,
    _if=any_changed(install_app, write_service),
)

nginx.site('templates/nginx/app.conf', host.data.app_domain)
