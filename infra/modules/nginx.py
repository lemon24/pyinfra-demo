from pyinfra.api import deploy
from pyinfra.operations import files
from pyinfra.operations import server
from pyinfra.operations.util import any_changed


@deploy("nginx site")
def site(template, domain, **context):

    write_site = files.template(
        name="write",
        src=template,
        dest=f'/etc/nginx/sites-available/{domain}',
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
        _if=any_changed(write_site, enable_site),
    )
