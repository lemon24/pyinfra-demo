from pyinfra import host
from pyinfra.operations import files

from modules import nginx

sync_files = files.sync(
    name="sync files",
    src='../home',
    dest='/opt/home',
    delete=True,
)

nginx.site('templates/nginx/home.conf', host.data.home_domain)
