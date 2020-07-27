![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)
![Push Container to Heroku](https://github.com/fbdevelopercircles/open-source-edu-bot/workflows/Push%20Container%20to%20Heroku/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Open Source Education Bot

Open Source Education Bot built by the Facebook Developer Circles community to help members contribute to open source projects.

# Installation


> **requirement**: python 3.6 or more


Start by cloning the repository locally and enter the project folder into your system.

```bash
git clone https://github.com/fbdevelopercircles/open-source-edu-bot
cd open-source-edu-bot
```

## Using a virtual environment:


```bash
python3 -m venv venv
```

On Windows

```PowerShell
py -3 -m venv venv
```

**Activate the environment**

Rename the environments file and adapt it:

```bash
cp .sample.env .env
```

On Windows:
```bash
copy .sample.env .env
```

Before you work on your project, activate the corresponding environment:

```bash
. venv/bin/activate
```

On Windows:
```PowerShell
venv\Scripts\activate
```

Your shell prompt will change to show the name of the activated environment.

**Install the require python package**

```bash
pip install -r requirements.txt
```

**Export environment variables**

```bash
export FLASK_APP fbosbot
export FLASK_RUN_HOST 0.0.0.0
export FLASK_ENV development
```

On Windows:
```bash
set FLASK_APP fbosbot
set FLASK_RUN_HOST 0.0.0.0
set FLASK_ENV development
```

**Compile the localization files**

```bash
cd src
pybabel compile -d locales
```

**To start the application locally run**

```bash
flask run
```

## Using Docker and docker-compose:

If you have docker and docker-compose installed in your computer, just run

```bash
docker-compose up -d
```

**Check your webhook with this command**

```bash
curl -X GET "<YOUR HOST>/webhook?hub.verify_token=<YOUR VERIFY TOKEN>&hub.challenge=CHALLENGE_ACCEPTED&hub.mode=subscribe&init_bot=true"
```
If your webhook verification is working as expected, you should see the following:

-```WEBHOOK_VERIFIED``` logged to the command line where your node process is running.\
-```CHALLENGE_ACCEPTED``` logged to the command line where you sent the cURL request.

Then check the logs to see if the profile is setup successfully!

CONTRIBUTORS
------------

## License

Open Source Education Bot is [MIT licensed](./LICENSE).
