![Open Source Love](https://badges.frapsoft.com/os/v2/open-source.svg?v=103)
![Push Container to Heroku](https://github.com/fbdevelopercircles/open-source-edu-bot/workflows/Push%20Container%20to%20Heroku/badge.svg)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

# Open Source Education Bot

Open Source Education Bot built by the Facebook Developer Circles community to help members contribute to open source projects.

## Installation

> **requirement**: python 3.6 or more

Start by fork and then cloning the repository locally and enter the project folder into your system.

```bash
git clone https://github.com/fbdevelopercircles/YOUR_GITHUB_USER_NAME/open-source-edu-bot 
```

where YOUR_GITHUB_USER_NAME is your GitHub handle.

```
cd open-source-edu-bot
git remote add upstream https://github.com/fbdevelopercircles/open-source-edu-bot
```

You can check that the previous command worked by running git remote -v. You should see the following output:
```
git remote -v
origin  https://github.com/YOUR_GITHUB_USER_NAME/open-source-edu-bot (fetch)
origin  https://github.com/YOUR_GITHUB_USER_NAME/open-source-edu-bot (push)
upstream        https://github.com/fbdevelopercircles/open-source-edu-bot (fetch)
upstream        https://github.com/fbdevelopercircles/open-source-edu-bot (push)
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

## Setting up your Messenger App
> **requirements**: 
>- **Facebook Page:**  Open-source-edu-bot will be only available for integration on a Facebook Page and not on your personal profile page.
To create a new page, visit https://www.facebook.com/pages/create .You can create a test page or a page with any suitable name.
>- **Facebook Developer Account:**  Required to create new apps, which are the core of any Facebook integration. You can register as a developer by going to the [Facebook Developers website](https://developers.facebook.com/) and clicking the "Get Started" button.
>- **Facebook App:** The Facebook app contains settings for your app like access tokens which are required in the .env file. To create a new app visit https://developers.facebook.com/ and click on **Add New App**

Now let's collect all tokens required for adapting your .env file .
1.  App_ID: Go to your app dashboard and then to Basic Settings, and now save your App_ID . \
You can also find your app [here](https://developers.facebook.com/apps/) 
2. APP_SECRET: Go to your app dashboard and then to Basic Settings, click on Show, enter your password and now save your APP_SECRET .
3. PAGE_ID: Go to your app Dashboard. Under Add Product find Messenger and click Set Up.\
Now you should be in the app Messenger Settings . 
Under Access Tokens, click on Add or Remove Page button and link your Facebook Page to your Messenger App. \
Now save your PAGE_ID which is displayed below your Page name under Access Tokens.
4. FB_PAGE_TOKEN: After completing Step 3, click on Generate Token button and now save your FB_PAGE_TOKEN.

## Testing the chatbot 

The chatbot can be tested here: https://m.me/OpenSourceChatbot before deploying it to your own page.

## How to contribute

The main purpose of this repository is to continue evolving open source. We want to make contributing to this project as easy and transparent as possible, and we grateful to the community for contributing bug fixes and improvements. Read below to learn how you can participate in improving Open Source Education Bot.

### [Code of Conduct][code]

Facebook has adopted a Code of Conduct that we expect project participants to adhere to.
Please read the [full text][code] so that you can understand what actions will and will not be tolerated.

[code]: ./CODE_OF_CONDUCT.md
### [Contributing Guide][contribute]

Read our [Contributing Guide][contribute] to learn about our development process, how to propose bugfixes and improvements, and how to build and test your changes to Open Source Education Bot.

[contribute]: ./CONTRIBUTING.md

### [Good First Issues][gfi]

We have a list of [good first issues][gfi] that contain bugs which have a relatively limited scope. This is a great place to get started, gain experience, and get familiar with our contribution process.

[gfi]: https://github.com/fbdevelopercircles/open-source-edu-bot/labels/good%20first%20issue

## Contributors

## License

Open Source Education Bot is [MIT licensed](./LICENSE).
