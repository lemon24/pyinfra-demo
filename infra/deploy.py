from pyinfra.operations import apt

apt.update(name="apt update", cache_time=24 * 3600)
