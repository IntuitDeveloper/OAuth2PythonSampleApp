[![Rate your Sample](views/Ratesample.png)][ss1][![Yes](views/Thumbup.png)][ss2][![No](views/Thumbdown.png)][ss3]

## OAuth 2.0 - Python 3 Sample App

The [Intuit Developer team](https://developer.intuit.com) has written this OAuth 2.0 Sample App in Python 3.5 with Django 1.10 to provide working examples of OAuth 2.0 concepts, and how to integrate with Intuit endpoints.

### Table of Contents

* [Getting Started](#getting-started)
* [Configuring your app](#configuring-your-app)
* [Run Your App](#run-your-app)
* [Project Structure](#project-structure)
* [Storing the Tokens](#storing-the-tokens)
* [Discovery document](#discovery-document)

### Getting Started

Before beginning, it may be helpful to have a basic understanding of OAuth 2.0 concepts.  There are plenty of tutorials and guides to get started with OAuth 2.0.

It is also expected that your development environment is properly set up for Python 3.5 and Django 1.10.

#### Setup

Clone the repository:
```
git clone https://github.com/IntuitDeveloper/OAuth2PythonSampleApp.git
```

Install Python 3.5:
```
https://www.python.org/
```

Install Django 1.10:
```
https://docs.djangoproject.com/en/1.10/releases/1.10/
```

Install Python Requests Library:
```
http://docs.python-requests.org/en/master/
```

OR use requirements.txt file:
```
cd OAuth2PythonSampleApp/
pip install -r requirements.txt 
```

Launch your app:
```
cd OAuth2PythonSampleApp/
python manage.py runserver
```

Your app should be running!  If you direct your browser to `http://localhost:8000/sampleappoauth2`, you should see the landing page. Please note - the app will not be fully functional until we finish configuring it.

### Configuring your app

All configuration for this app is located in [settings.py](OAuth2DjangoSampleApp/settings.py).  Locate and open this file.

We will need to update 2 items:

- `CLIENT_ID`
- `CLIENT_SECRET`

All of these values must match **exactly** with what is listed in your app settings on [developer.intuit.com](https://developer.intuit.com).  If you haven't already created an app, you may do so there.  Please read on for important notes about client credentials, scopes, and redirect urls.

#### Client Credentials

Once you have created an app on Intuit's Developer Portal, you can find your credentials (Client ID and Client Secret) under the "Keys" tab.  You will also find a section to enter your Redirect URI here.

#### Redirect URI

Update your app settings on the Developer Portal ("Keys" section) with the correct Redirect URI: `http://localhost:8000/sampleappoauth2/authCodeHandler`. 

Note: Using localhost and http will only work when developing, using the sandbox credentials. Once you use production credentials, you'll need to host your app over https.

#### Scopes

While you are in [settings.py](OAuth2DjangoSampleApp/settings.py), you'll notice the scope sections.

```
  ACCOUNTING_SCOPE = 'com.intuit.quickbooks.accounting'
  OPENID_SCOPES = ['openid','profile','email','phone','address']
```
  It is important to ensure that the scopes your are requesting match the scopes allowed on the Developer Portal.  For this sample app to work by default, your app on Developer Portal must support both Accounting and OpenID scopes.
  
  Note: The scope for Payments API is ```com.intuit.quickbooks.payment```

----------

### Run your app

After setting up both Developer Portal and your [settings.py](OAuth2DjangoSampleApp/settings.py), try launching your app again!  All flows should work.  The sample app supports the following flows:

**Sign In With Intuit** - this flow requests OpenID only scopes. After clicking on the 'Sign In With Intuit' button from the homepage it will end up on a Connected page displaying all the information that you requested via the OpenId scopes.

**Connect To QuickBooks** - this flow requests non-OpenID scopes. You will be able to make a QuickBooks API sample call (using the OAuth2 token) on the connected page. Sample implementation for RefreshToken and RevokeToken is also available in that page.

**Get App Now** - this flow requests both OpenID and non-OpenID scopes. It simulates the request that would come once a user clicks "Get App Now" on the apps.com website, after you publish your app.

----------

### Project Structure

In order to find the code snippets you are interested in, here is how the code is organized.

#### sampleAppOAuth2/views.py

This views.py file contains all of the main Django routes that handle button clicks such as the Connect To Quickbooks, Sign In With Intuit and Get App Now buttons. It also contains the redirect URI (/sampleappoauth2/authcodehandler) which will grab the OAuth2.0 Auth code, exchange it for a Bearer token before redirecting either to the connected page depending on whether the user is doing an OpenId flow or a Non-OpenId flow.

#### sampleAppOAuth2/services.py

This services.py file contains all of the core logic of the application. Mainly, outbound requests to Intuit's Services such as QBO V3 APIs and the Intuit User Profile service. Here you will find examples of how to call these Intuit services using the Python Requests library and handle their JSON responses.

### Storing the tokens
This app stores all the tokens and user information in the session. For production ready app, tokens should be encrypted and stored in a database.

### Discovery document
The app calls the discovery API during startup and loads all the endpoint urls. For production ready app, make sure to run this API once a day to get the latest urls.

[ss1]: #
[ss2]: https://customersurveys.intuit.com/jfe/form/SV_9LWgJBcyy3NAwHc?check=Yes&checkpoint=OAuth2PythonSampleApp&pageUrl=github
[ss3]: https://customersurveys.intuit.com/jfe/form/SV_9LWgJBcyy3NAwHc?check=No&checkpoint=OAuth2PythonSampleApp&pageUrl=github
