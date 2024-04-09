# The Book

Application for administrative control of
[*Laboratório Hacker de Campinas*](https://lhc.net.br), a hackerspace located in
[Campinas, SP, Brazil](https://www.openstreetmap.org/search?query=Laborat%C3%B3rio%20Hacker%20de%20Campinas#map=19/-22.91780/-47.05245).

It is a (not complete) single-entry bookkeeping system with some particularities
that are suitable for accounting management of the hackerspace. However, we believe
that this application can be used by any small association that wants to track
the origin and the destination of the money received.

## Development

### Local environment

We suggest the use of [pyenv](https://github.com/pyenv/pyenv) to manage your Python
version and create an isolated environment where you can safely develop. After installing
it, you can prepare the environment using the following commands:

```
$ pyenv virtualenv 3.11.5 myvenv
$ pyenv activate myvenv
$ python -m pip install -r requirements.txt
```

Now you are ready to start development.

### Running

Before running the application locally for the first time (or after creating a
new database migration), you need to run the following command:

```
$ python manage.py migrate
```

You can start the application it using the following command:

```
$ cd src
$ python manage.py runserver
```

Then you should be able to access it at http://127.0.0.1:8000

To create a superuser to have access to Django Admin (http://127.0.0.1:8000/admin),
use the following command and answer its questions:

```
$ python manage.py createsuperuser
```

## Deployment

Application is running in a [fly.io](https://fly.io/) account. If you are planning to
update the production version, ask some member of LHC board to get access credentials.
Our account username is `contato@lhc.net.br`.

Se [Django docs](https://docs.djangoproject.com/en/5.0/howto/deployment/) if you want to deploy
in a different platform.

Production database is a PostgreSQL managed by [fly.io](https://fly.io/docs/postgres/). Check
its documentation to know how to use it.

### Authentication

Before start using [fly.io](https://fly.io/), you need to authenticate with the right credentials. Use
the command bellow and follow the instructions:

```
$ flyctl auth login
```

### Configuration

To set/update the environment variables to configure the applications (secret keys,
database URL, etc.), you can use fly.io dashboard or use the following command for
each variable you want to set:

```
flyctl secrets set VARIABLE_NAME="value"
```

You can see the list of secrets configured using the command:

```
flyctl secrets list
```

You can also set environment variables that will be deployed in `[env]` section
of `fly.toml`. **Don't commit any value that shouldn't be public (like database credentials)**


### Production Deploy

When everything is configured as desired, deploy to production using the command:

```
flyctl deploy --verbose
```

### Useful commands

- Application status

```
flyctl status
```

- Application logs

```
flyctl logs
```

- Application console

```
flyctl ssh console -C bash
```

> If you see the error message `Error: app thebook has no started VMs.` it means
> that there is no machine running the application. Just access the application in
> your browser (so a new VM is started) and try again.