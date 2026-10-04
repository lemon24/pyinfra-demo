from pyinfra.operations import apt
from pyinfra.operations import files
from pyinfra.operations import server

apt.update(name="apt update", cache_time=24 * 3600)

apt.packages('nginx', name="install nginx")

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
