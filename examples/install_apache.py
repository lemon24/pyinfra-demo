from pyinfra import host
from pyinfra.facts.server import LinuxName
from pyinfra.operations import server

if host.get_fact(LinuxName) in ['Ubuntu', 'Debian']:
    server.packages('apache2')
else:
    server.packages('httpd')
