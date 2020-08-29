# Development: Getting Started

## With Mac OS and brew

Tested on 10.12.6.

Install Docker tools and create a docker-machine:
```
brew install docker docker-compose docker-machine
docker-machine create polyledger
eval $(docker-machine env polyledger)
```

Then you need a `.env.development` at the root of the project, that will contain environment variables needed by `docker-compose` and Django.

```
docker-machine env polyledger > .env.development
```

To generate a secret key for Django, use `python -c "import string,random; uni=string.ascii_letters+string.digits+string.punctuation; print repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))]))"`.

Example of an `.env.development`:

```
DOCKER_TLS_VERIFY="1"
DOCKER_HOST="tcp://192.168.99.100:2376"
DOCKER_CERT_PATH="/Users/mpigassou/.docker/machine/machines/polyledger"
DOCKER_MACHINE_NAME="polyledger"

SECRET_KEY=yj1^cc7-tmpyr+xqt6n&1da!epea3@l_l6jj(@aa!_p_3d+tqi
EMAIL_HOST_PASSWORD=foobar

# Settings module will vary depending on the environment
DJANGO_SETTINGS_MODULE=polyledger.settings.local
```

### Project setup

```
docker-compose up
```

The first time, you should get some errors, but it should at least run the migrations and run `npm install`.
Exit with ctrl+c.

```
docker-compose build
```

You need to rebuild because you installed some libraries.

```
docker-compose up
```

This time, everything should be fine.