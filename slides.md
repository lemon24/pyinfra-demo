<!--

caffeinate -dimsut 3600 &
cd ~/code/pyinfra-demo
./run.sh reset
alias co="$( pwd )/run.sh checkout"
PS1='%1~ %(#.#.$) '
function precmd { echo; echo }
clear

-->


# pyinfra – simple infrastructure automation in Python

... in which we live demo `pyinfra`.


## About me

Hello, my name is [REDACTED].

I worked at [REDACTED] for most of my career:

* SRE for reverse proxy behind [REDACTED] and 2k+ other websites
* built a data lake + feature store for the [REDACTED] ML organization

In my spare time, I:

* write at `death.andgravity.com`, mostly about Python
* created `lemon24/reader`, a feed reader library + web app


## What is pyinfra?

> pyinfra turns Python code into shell commands
> and runs them on your servers. [in parallel]

Think Ansible, but simpler.

```python
# deploy.py

for user in ['admin', 'alice', 'bob']:
    server.user(user)

files.put('files/hello.txt', '/etc/motd')

if host.data.get('install_postgres'):
    apt.install('postgresql')

```


## Why use pyinfra?

* declarative and idempotent
* infrastructure as actual code, not YAML
* custom operations in 10 lines
* works on any host you can SSH into
* concurrent, "6× faster than Ansible"
* scales to "thousands of servers"


## When to use pyinfra?

If you configure servers over SSH:

* cloud-optional / cloud-agnostic architecture
* one-computer / one-process programming
* self-hosting / home server

...but maybe not if you need more than push over SSH:

* fully automated pipelines
* big / multiple teams


## The demo

Code available at <https://github.com/lemon24/pyinfra-demo>.

Beta (single VM):

    .--- pyinfra.local ---.- app.pyinfra.local -.
    |                   nginx                   |
    |   static website    :   Python web app    |
    '-------------------------------------------'

Prod (two Hetzner servers):

    .--- pyinfra.a.c ----. .- app.pyinfra.a.c --.
    |       nginx        | |       nginx        |
    |   static website   | |   Python web app   |
    '--------------------' '--------------------'

```shell
kate infra/deploy.py
```


## Operations and facts

Use operations to *ensure state*:

```shell
cat examples/create_file.py
pyinfra @local examples/create_file.py
```

Use facts to *gather data*:

```shell
cat examples/install_apache.py
pyinfra @local examples/install_apache.py --dry
```


## Where are the commands?

Simplified implementation of `files.file`:

```python
@operation()
def file(path: str, present: bool = True):

    # read current host state using facts
    info = host.get_fact(File, path=path)

    # diff current state against desired state
    if info is None and present:
        # maybe yield commands to reach desired state
        yield f"touch {quote(path)}"

    elif info and not present:
        yield f"rm -f {quote(path)}"
```

Two execution phases, *prepare* and *execute*:

```shell
cat examples/delete_file.py
pyinfra @local examples/delete_file.py --debug
```


## Initial nginx setup

<!-- co fix && cd infra -->

An inventory contains groups of hosts:

```shell
cat inventories/beta.py
pyinfra inventories/beta.py exec uptime
```

A deploy contains operations:

```shell
kate deploy.py
pyinfra inventories/beta.py deploy.py
```

Deploy code runs once per host, in the prepare phase.


## Static website

<!-- co @deploy -->

Simple static landing page:

```shell
kate tasks/home.py inventories/beta.py deploy.py
```

Reuse via packaged deploys and template inheritance:

```shell
kate modules/nginx.py
kate templates/nginx/{home,http}.conf
pyinfra inventories/beta.py deploy.py --diff
open http://pyinfra.local:2080/
```


## Python web app

<!-- co secret && tree ../app -->

Simple Flask web app served by nginx + Gunicorn:

       :80, :443
           |
    .-------------.
    |    nginx    |  groups: app-socket, www-data
    '-------------'
           |
        app.sock     groups: app-socket
           |
    .- Gunicorn --.
    |   web app   |  groups: app-socket, app
    '-------------'

```shell
kate tasks/app.py
```


## Handling secrets

Problem: can't store secrets directly in the repository.
Solution: get them from somewhere else during the deploy.

```shell
kate templates/config.py.jinja modules/secrets.py
pyinfra inventories/beta.py deploy.py -y && open http://app.pyinfra.local:2080/
```


## HTTPS using certbot

<!-- co -->

Custom operation that gets Let's Encrypt certificates:

```shell
kate modules/nginx.py modules/certbot.py
```

Problem: can't test this in a VM.
Solution: test in prod. ಠ_ಠ

```shell
cat inventories/prod.py
pyinfra inventories/prod.py deploy.py -y && open https://{,app.}pyinfra.andgravity.com/
```
