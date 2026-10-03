from pyinfra import host
from pyinfra.operations import apt
from pyinfra.operations import files
from pyinfra.operations import server

for user in ['admin', 'alice', 'bob']:
    server.user(user)

files.put('files/hello.txt', '/etc/motd')

if host.data.get('install_postgres'):
    apt.install('postgresql')
