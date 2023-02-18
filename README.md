# sol-tax-webapp

This tool is meant for use by Virginia localities to help them decide which taxation model to use for solar generating facilities, either the new Revenue Share model, or the old M&T/Real Estate tax model. The tool allows users to create different analyses of solar projects of various electric capacities and land sizes. It provides a user a detailed analysis of the expected revenues of a solar project under both tax models as well as a total summary of the revenues for all projects under both tax models. 

Link to Live Site: [https://solar-tax-webapp.herokuapp.com/](https://solar-tax-webapp.herokuapp.com/)

**Sections**

1. [Github](#2ga15kwy16nx)
2. [Python](#scoqj6sek23g)
3. [Django](#i6x9imrr2t08)
  - Setup including virtual environment
  - How it works/ File Structure
4. [Heroku](#zho0313diu0q)
5. [PostgreSQL](#q5yts6g2ir2u)
6. [Gmail](#o16f2efg332b)
7. [Admin Site](#ixt6gngx859q)
8. [Local Development](#h22fw0m05rg4)

**Github**
Any changes made to the master branch are automatically pushed into the live server through Heroku. Make sure changes are working properly before pushing to the master branch. Commit changes to branches other than master branch then merge when appropriate. Make sure you commit changes frequently to save changes to GitHub.

**Python**

Need Python 3 or later, developed using Python 3.8.1

[https://www.python.org/downloads/](https://www.python.org/downloads/)

**Django**

[https://www.djangoproject.com/](https://www.djangoproject.com/)

Django is a Python web framework meant for rapid development.

SolTax was developed using Django 3.1

Installing Django: [https://docs.djangoproject.com/en/3.1/topics/install/#installing-official-release](https://docs.djangoproject.com/en/3.1/topics/install/#installing-official-release)

Django Tutorial: [https://docs.djangoproject.com/en/3.1/intro/tutorial01/](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

A. Project Setup

1. Create a virtual environment. This means the local soltax project is in a dedicated directory with specific versions of all libraries needed for the application.
2. Project was created using the pipenv virtual environment which can be found [here](https://pypi.org/project/pipenv/). Pipenv should be used again as the repository has a Pipfile and Pipfile.lock which contains information about the libraries needed for the project.
  - To activate the virtual environment when setup enter pipenv shell into the terminal
  - To exit the virtual environment, type exit.
3. When the virtual environment is activated you can then install Django.
4. To install all libraries needed for the project, use _pip install -r requirements.txt_, if you are using pip. This will install all packages that are listed in the requirements file.
5. You will need to set up a local PostgreSQL database to use for local development. Follow [this](https://djangocentral.com/using-postgresql-with-django/) guide and you should be good.
  1. These are the parameters used for local database and are located in settings.py. Use these to set up your local database. They are found in _settings.py_.
  - &#39;ENGINE&#39;: &#39;django.db.backends.postgresql\_psycopg2&#39;,
  - &#39;NAME&#39;:&#39;soltax&#39;,
  - &#39;USER&#39;: &#39;soltaxuser&#39;,
  - &#39;PASSWORD&#39;: &#39;password&#39;,
  - &#39;HOST&#39;: &#39;localhost&#39;,
  - &#39;PORT&#39;: &#39;&#39;,
6. To test that the project has been set up properly on your local machine, type _python manage.py runserver_ to run the web application locally. If no errors appear in the terminal visit _localhost:8000_ or [_http://127.0.0.1:8000/_](http://127.0.0.1:8000/) to view the site.

B. File Structure

The project has three main components

1. The Django Project, which is contained in the SolarTax folder.
2. An app which contains the code for what the web application should do, this is the models folder.
3. Other files needed for Heroku, Github, and the virtual environment.

SolarTax Folder - Only these three files should be changed.
  1. Settings.py - Defines all the Django settings needed for the project. If you install a new dependency, you may have to add it to INSTALLED\_APPS.
  2. Asgi.py - Spins up an instance of the application and uses the settings as defined in the settings.py file.
  3. Wsgi.py - Spins up an instance of the application and uses the settings as defined in the settings.py file. Used for the Heroku site
  4. Urls.py - Defines the admin url, urls that authenticate users which are defined by Django, a url that makes it possible to display a graph for each project analysis, and then any url that is defined in the models app.

Models - Django application which follows the MVT framework. MVT framework stands for model-view-template. Models are effectively classes that you would find in Java, Python, or C++. Models require certain variables to be defined about them when instantiated. The views take in information from models and request data (&quot;GET&quot; or &quot;POST&quot; methods) and determine what to do with this information. They then pass information to a template. The template is the html that defines how to display the information received by the views, although it has a bit more functionality compared to straight html as you can pass variables in and use for loops.
  1. Admin.py - tells the admin site to include information about all the models in the project. The admin site allows us to view all data of the project.
  2. Apps.py - defines this app to be named models
  3. Forms.py - defines any forms that are used throughout the project. Most are tied to a model so they can create an instance of a model through a submission of a form. [https://docs.djangoproject.com/en/3.1/topics/forms/](https://docs.djangoproject.com/en/3.1/topics/forms/)
  4. Models.py - Defines the UserProfile, Locality, Simulation, and Calculation models. A UserProfile is tied to one Localily, and has many simulations. A Locality can be tied to any number of UserProfiles. A Simulation is only tied to one UserProfile and only has one Calculation model associated with it. A Calculation instance is tied to one Simulation instance. Feedback is a model that holds an email and a text field containing feedback or a question. It is not tied to any other model.
  5. Revenue\_calculations.py - Python file that has functions to calculate the revenue for projects based on the input parameters.
  6. Urls.py - Defines the URLs that are valid for the web application and which view corresponds to the URL entered.
  7. Views.py - Defines the different views needed for the web application. This is the business logic that is needed to get parameters from instances of models or forms and then transform the data if necessary to pass onto the HTML templates to display the web page correctly.
  8. Templates Folder - This folder contains the HTML template files that are used when a view calls for a template to display with the necessary parameters. _Base.html_ is a HTML file that contains code that is to be used as a base for the site so all pages have the same basic design.
    1. The registration sub-folder contains the templates that are used for the password reset functionality of the web application.
  9. Static Folder - This folder contains any images that are displayed on the site and the CSS and JS files used to further design the pages of the web application. Add any new images into this folder and continue to edit the CSS and JS files in this folder if needed.
  10. Templatetags Folder - The _custom\_tags.py_ file defines tags that can be used in the HTML templates to manipulate data if necessary from variables that are passed into the templates.

Other Files
  1. Feedback\_sender.py - This file is used to send an email to Elizabeth, Carrie, and Thomas at 3pm each weekday, if someone submitted feedback through the web application. This also pings the website 3 times an hour each weekday from 9-5 so the dyno on heroku is constantly up in this time period. This means loading times should be faster.
  2. Manage.py - Django file that boots the application up when called. Don&#39;t touch unless absolutely necessary.
  3. Pipfile and Pipfile.lock - These files are for the virtual environment and heroku and list all the dependencies of the project and the versions used.
  4. Procfile - A heroku file that gets the web application running on heroku. It runs python manage.py migrate to make any migrations necessary to the database. It then runs the application with the wsgi.py file and finally creates a cron job to run feedback\_sender.py
  5. Requirements.txt - file that lists all dependencies is to be used to automatically install all dependencies at once. Keep updated with any new dependencies that are added.

**Heroku**

Login

The SolTax project is the only project in the profile under the name solar-tax-webapp.

To add new collaborators to the project click the &quot;manage access&quot; button on the project overview page and add the email address of the person to add to the project.

To view Postgres database information select &quot;Heroku Postgres&quot; under Installed add-ons. This will open a new page just for the database. The database credentials are under &quot;settings&quot; and then &quot;database credentials&quot;

There is a Heroku CLI (command line interface) to interact with Heroku from the terminal, link is [here](https://devcenter.heroku.com/articles/heroku-cli).

Heroku has config variables saved which are necessary for the application and should not be shared with anyone outside of the organization or be placed in the code. These config variables are listed under &quot;Settings&quot; and then &quot;Config Vars&quot;. To view them select &quot;Reveal Config Vars&quot;.

The DATABASE\_URL is the url needed to access the PostgreSQL database for the live site. The two EMAIL\_HOST\_\*\*\*\* variables are the login information for the email that is used to send email notifications for feedback that is submitted. The STAKEHOLDER\_EMAIL\_\* variables are the emails where the email notifications are sent from feedback. To add your own email to receive these notifications and your email as a config var and edit _feedback\_sender.py_ to get the email and add it to the send\_mail function. The final config var is SECRET\_KEY this is used for security purposes more information can be found [here](https://docs.djangoproject.com/en/3.1/ref/settings/#std:setting-SECRET_KEY).

**PostgreSQL**

This project uses a PostgreSQL database. You will need access to two databases, one for local development and testing, and access to the database for the live server.

To download PostgreSQL visit their page [here](https://www.postgresql.org/download/).

To connect to the live server database you need to get the database credentials from the Heroku page as described in the Heroku section above.

For a local database follow the guide that was laid out in step 5 of "Project Setup" above.
**Gmail**

There is a gmail account for use on this project. 

The sole purpose of this email is to send emails to users for password reset and to send Thomas, Carrie, and Elizabeth emails about feedback received.

**Admin Site**

Both the local and live sites have access to an admin site. These sites need a username and password. For your local server you need to create a superuser that can access the admin site. To do this you need to type _python manage.py createsuperuser_ into the command line while in the project directory. Fill out the command line prompts and then to access the admin site run the application using _python manage.py runserver_, go to localhost:8000/admin or _http://127.0.0.1:8000/_admin and sign in. For the live server there is already a superuser created with credentials. Contact XXXXXXXX at [xxxxx@virginia.edu](mailto:xxxxx@virginia.edu) for admin site login information. To get to the live server admin site visit https://solar-tax-webapp.herokuapp.com/admin/ 

The admin site allows us to manually view all instances of any models created by users and allows us to change the parameter values if needed.

**Local Development**

Before running a local server create a new directory named hiddenVars with 3 files named secret_key.txt, email.txt, and email_password.txt. Put the correct variables that can be found on the Heroku site into these files. This helps set the correct settings variables for the local server. Also make sure that DEBUG is set to True and ALLOWED_HOSTS = [] before running a local server. DEBUG should be set to False and ALLOWED_HOSTS = ['solar-tax-webapp.herokuapp.com', 'localhost:8000', '127.0.0.1:8000'] for the live server.

For local development make sure you are in the virtual environment you created for the project. Also before running the local server make sure you are located in the same directory as the _manage.py_ file. If you are not, you will not be able to run the local server. Make changes to the project as you see fit, then run your local server using _python manage.py runserver._ Test out the new feature on the local development server and add test cases to tests.py to ensure it does not impact other aspects of the project. Make sure to commit to the github repo consistently on a development branch to ensure progress is saved. Merge to the master branch when appropriate and this will automatically push all updates onto the live Heroku server. To make sure the Heroku server is created successfully after a change to the master branch is made, visit the project homepage and you will see the project being built on Heroku and then deployed.
