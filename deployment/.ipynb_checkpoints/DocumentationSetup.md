# Deployment: Docker Compose on DigitalOcean

This wiki entry describes a deployment process to a DigitalOcean droplet using Python 3.5.

## Step 1: Create droplet

Log into DigitalOcean and create or use an existing droplet running Ubuntu 16.04.

Make sure you:
- Use an SSH key
- Give the droplet a descriptive name

<kbd>![](https://cl.ly/0R0k0M3D3R3s/Image%202018-05-16%20at%203.19.23%20PM.png)</kbd>

## Step 2: Configure Ubuntu

SSH into the droplet:

```
ssh root@<ip>
```

You will be asked to update the root password.

It is recommended to create a user with restricted permissions. (For now, please refer to [this guide](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04#step-two-%E2%80%94-create-a-new-user).)

Install Node.js:

```
cd ~
curl -sL https://deb.nodesource.com/setup_8.x -o nodesource_setup.sh
bash nodesource_setup.sh
apt-get install nodejs
nodejs -v
npm -v
apt-get install build-essential
rm nodesource_setup.sh
```

Install Docker:

```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
apt-get update
apt-cache policy docker-ce
apt-get install -y docker-ce
systemctl status docker
```

Install Docker Compose:

```
curl -L https://github.com/docker/compose/releases/download/1.18.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
docker-compose --version
```

## Step 3: Clone the application

Clone the GitHub repository in the home folder:

```
cd /home && git clone https://github.com/polyledger/polyledger.git
```

You will be prompted for a GitHub username and password/access token.

## Step 4: Create web client production build

Install the web client dependencies and create a production build:

```
cd /home/polyledger/web_client
NPM_TOKEN=<NPM_TOKEN> npm install
npm run build
```

## Step 5: Start Docker Compose

Create a environment variable file:

```
touch /home/polyledger/.env.production
nano /home/polyledger/.env.production
```

To generate a secret key, run this command in any shell:

```
python -c "import string, random; uni=string.ascii_letters+string.digits+string.punctuation; print(repr(''.join([random.SystemRandom().choice(uni) for i in range(random.randint(45,50))])))"
```

Now save these variables:

```
DJANGO_SETTINGS_MODULE=polyledger.settings.production
PYTHON_ENV=production
SECRET_KEY=<SECRET_KEY>
EMAIL_HOST_PASSWORD=<EMAIL_HOST_PASSWORD>
NPM_TOKEN=<NPM_TOKEN>
BITBUTTER_API_KEY=<BITBUTTER_API_KEY>
BITBUTTER_API_SECRET=<BITBUTTER_API_SECRET>
BITBUTTER_BASE_URI=<BITBUTTER_BASE_URI>
BITBUTTER_PARTNERSHIP_ID=<BITBUTTER_PARTNERSHIP_ID>
BITBUTTER_PARTNER_ID=<BITBUTTER_PARTNER_ID>
```

Build the Docker images and start the services:

```
docker-compose -f production.yml build
docker-compose -f production.yml up
```

## Step 6: Create an admin user

First we need to copy the container ID of the `polyledger_server` image:

```
docker ps
```

Now run the `createsuperuser` command in the `polyledger_server` container:

```
docker exec -it <CONTAINER_ID> python manage.py createsuperuser
```

You will be prompted to create an admin user.

```
Email address: admin@polyledger.com
First name: Satoshi
Last name: Nakamoto
Password:
Password (again):
Superuser created successfully.
```

Navigate to `http://<SERVER_IP>/admin/login/` in your browser and login with the credentials you just created.

## Step 7: Add coins

Currently you have to add coins with their symbol and name to fetch prices for them. This will be simplified in the future.

<kbd>![](https://cl.ly/0r380K280v41/download/[8e281bb0816e59ed782f0e0daa5c60d8]_Image%202018-05-17%20at%2012.05.35%20PM.png)</kbd>

Once you have added some coins, move onto the next step.

<kbd>![](https://cl.ly/1M2x1i2I3I1J/Image%202018-05-17%20at%2012.07.36%20PM.png)</kbd>

## Step 8: Fetch coin prices

The easiest way would be to stop Docker Compose with <kbd>CTRL</kbd> + <kbd>C</kbd> and then restart:

```
docker-compose -f production.yml up
```

## Step 9: Add CloudFlare DNS

Log into [CloudFlare](https://cloudflare.com) and create a DNS A record for the server's IP using the "portfolio" subdomain. This enables DNS routing and enables HTTPS.

<kbd>![](https://cl.ly/3u3e3O3a0c2u/[739a95d8a3b634969d55c663a199bce9]_Image%202018-05-17%20at%2012.13.49%20PM.png)</kbd>

## Step 10: Whitelist emails

Before anyone can sign up on the app, their email has be to whitelisted in the admin interface. Make sure you add the email to the whitelist before signing up or you will receive a "Forbidden" error.

## Step 11: Add the site

Make sure you add the site domain in the admin interface so Django knows the domain.

<kbd>![](https://cl.ly/2Z0S1D2E2h1A/[5acb2233d1b08d37f037ca120a5692c0]_Image%202018-05-17%20at%201.08.17%20PM.png)</kbd>

## Step 12: Test the portfolio app

Now you can start testing the portfolio app. Log out of the admin interface and navigate to [https://portfolio.polyledger.com/signup](https://portfolio.polyledger.com/signup) in your browser.

---

## References
- [Initial Server Setup with Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/initial-server-setup-with-ubuntu-16-04)
- [How to Install Node.js on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-node-js-on-ubuntu-16-04)
- [How to Install and Use Docker on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-16-04)
- [How to Install Docker Compose on Ubuntu 16.04](https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-16-04)