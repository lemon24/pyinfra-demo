from pyinfra import host
from pyinfra.facts.files import Link
from pyinfra.operations import apt
from pyinfra.operations import files
from pyinfra.operations import server

apt.update(name="apt update", cache_time=24 * 3600)

apt.packages('nginx', name="install nginx")

if host.get_fact(Link, '/etc/nginx/sites-enabled/default'):
    files.link(
        name="disable default site",
        path='/etc/nginx/sites-enabled/default',
        present=False,
    )
    server.service(
        name="reload nginx",
        service='nginx',
        reloaded=True,
    )
