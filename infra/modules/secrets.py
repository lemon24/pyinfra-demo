import json

from pyinfra import host

secrets_path = 'secrets.json'


def get_secret(name, *, stage=None):
    if not stage:
        stage = host.data.stage

    with open(secrets_path) as f:
        data = json.load(f)

    if secret := data.get(stage, {}).get(name):
        return secret

    raise RuntimeError(f"secret {name!r} for stage {stage!r} not found")
