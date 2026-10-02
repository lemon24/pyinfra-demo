from pyinfra import host
from pyinfra.operations import files
from pyinfra.operations import server
from pyinfra.operations.util import any_changed

sync_files = files.sync(
    name="sync files",
    src='../home',
    dest='/opt/home',
    delete=True,
)

domain = host.data.home_domain

write_site = files.template(
    name="write site",
    src='templates/nginx/home.conf',
    dest=f'/etc/nginx/sites-available/{domain}',
    domain=domain,
)
enable_site = files.link(
    name="enable site",
    path=f'/etc/nginx/sites-enabled/{domain}',
    target=f'/etc/nginx/sites-available/{domain}',
)

server.service(
    name="reload nginx",
    service='nginx',
    reloaded=True,
    _if=any_changed(write_site, enable_site),
)
