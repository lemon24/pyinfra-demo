from pyinfra import host
from pyinfra.api import deploy
from pyinfra.operations import files
from pyinfra.operations import server
from pyinfra.operations.util import any_changed

from . import certbot


@deploy("nginx site")
def site(template, domain, https=None, **context):
    reload_ops = []

    if https is None:
        https = host.data.get('nginx_https')
    if https:
        reload_ops.append(certbot.certificate(domain, name="cert"))

    write_site = files.template(
        name="write",
        src=template,
        dest=f'/etc/nginx/sites-available/{domain}',
        base=f"templates/nginx/http{'s' if https else ''}.conf",
        domain=domain,
        **context,
    )
    enable_site = files.link(
        name="enable",
        path=f'/etc/nginx/sites-enabled/{domain}',
        target=f'/etc/nginx/sites-available/{domain}',
    )

    server.service(
        name="reload",
        service='nginx',
        reloaded=True,
        _if=any_changed(write_site, enable_site, *reload_ops),
    )
