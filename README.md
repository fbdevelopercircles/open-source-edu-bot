![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)
![Push Container to Heroku](https://github.com/fbdevelopercircles/open-source-edu-bot/workflows/Push%20Container%20to%20Heroku/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Open Source Education Bot

Open Source Education Bot built by the Facebook Developer Circles community to help members contribute to open source projects.

## Installation

> **requirement**: python 3.6 or more

Start by cloning the repository locally and enter the project folder into your system.

```bash
git clone https://github.com/fbdevelopercircles/open-source-edu-bot
cd open-source-edu-bot
```

## Setting up the environment:

**Create the virtual environment**

```bash
python3 -m venv venv
```

On Windows

```PowerShell
py -3 -m venv venv
```

**Activate the virtual environment**

Before you work on your project, activate the corresponding environment:

```bash
. venv/bin/activate
```

On Windows:
```PowerShell
venv\Scripts\activate
```

Your shell prompt will change to show the name of the activated environment.

**Install the required python packages**

```bash
pip install -r requirements.txt
```

**Set up the environment variables**  

Navigate to the src folder(root directory of the project):

```bash
cd src
```

Copy the environments file and adapt it:

```bash
cp .sample.env .env
```

On Windows:
```bash
copy .sample.env .env
```

**Compile the localization files**

```bash
pybabel compile -d locales
```

**To start the application locally run**

```bash
flask run
```

## Using Docker and docker-compose

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

## Testing the chatbot 

The chatbot can be tested here: https://m.me/OpenSourceChatbot before deploying it to your own page.

## How to contribute

The main purpose of this repository is to continue evolving open source. We want to make contributing to this project as easy and transparent as possible, and we grateful to the community for contributing bug fixes and improvements. Read below to learn how you can participate in improving Open Source Education Bot.

### [Code of Conduct][code]

Facebook has adopted a Code of Conduct that we expect project participants to adhere to.
Please read the [full text][code] so that you can understand what actions will and will not be tolerated.

[code]: https://code.fb.com/codeofconduct/

### [Contributing Guide][contribute]

Read our [Contributing Guide][contribute] to learn about our development process, how to propose bugfixes and improvements, and how to build and test your changes to Open Source Education Bot .

[contribute]: ./CONTRIBUTING.md

### [Good First Issues][gfi]

We have a list of [good first issues][gfi] that contain bugs which have a relatively limited scope. This is a great place to get started, gain experience, and get familiar with our contribution process.

[gfi]: https://github.com/fbdevelopercircles/open-source-edu-bot/labels/good%20first%20issue

## Contributors

## License

Open Source Education Bot is [MIT licensed](./LICENSE).
