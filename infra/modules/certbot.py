from shlex import quote

from pyinfra import host
from pyinfra.api import FactBase
from pyinfra.api import operation


@operation()
def certificate(domain):

    if domain in host.get_fact(Certificates):
        return

    yield f"certbot certonly -d {quote(domain)} -n --nginx --agree-tos"


class Certificates(FactBase):
    default = dict
    requires_command = "certbot"

    def command(self):
        return "certbot certificates"

    def process(self, output):
        return {c['name']: c for c in _parse_certbot_certificates(output)}


def _parse_certbot_certificates(lines):
    cert = {}
    for line in lines:
        key, sep, value = line.strip().partition(': ')
        if not sep:
            continue
        match key:
            case 'Certificate Name':
                if cert:
                    yield cert
                    cert = {}
                cert['name'] = value
    if cert:
        yield cert
