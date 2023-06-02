# SolTax WebApp
This tool is meant for use by Virginia localities to help them decide which taxation model to use for solar generating facilities, either the new Revenue Share model, or the old M&T/Real Estate tax model. The tool allows users to create different analyses of solar projects of various electric capacities and land sizes. It provides a user a detailed analysis of the expected revenues of a solar project under both tax models as well as a total summary of the revenues for all projects under both tax models. 

SolTax WebApp: [https://solar-tax-webapp.herokuapp.com/](https://solar-tax-webapp.herokuapp.com/)

## Sections
1. [Getting Started](#getting-started)
2. [Structure](#structure)
3. [Development](#development)

## Getting Started
### Github
Any changes made to the master branch are automatically pushed into the live server on Azure. Make sure changes are working properly before pushing to the master branch. Commit changes to branches other than master branch then merge when appropriate. Make sure you commit changes frequently to save changes to GitHub.

### Python
Need Python 3 or later (Developed using Python 3.8.1)

__Python Documentation__: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### Django
Django is a Python web framework meant for rapid development. SolTax WebApp was developed using Django 3.1.

__Django Documentation__: [https://www.djangoproject.com/](https://www.djangoproject.com/)

__Installing Django__: [https://docs.djangoproject.com/en/3.1/topics/install/#installing-official-release](https://docs.djangoproject.com/en/3.1/topics/install/#installing-official-release)

__Django Tutorial__: [https://docs.djangoproject.com/en/3.1/intro/tutorial01/](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

### Admin Site
Both the local and live sites have access to an admin site. These sites need a username and password. For your local server you need to create a superuser that can access the admin site. To do this you need to type _python manage.py createsuperuser_ into the command line while in the project directory. Fill out the command line prompts and then to access the admin site run the application using _python manage.py runserver_, go to localhost:8000/admin or _http://127.0.0.1:8000/_admin and sign in. For the live server there is already a superuser created with credentials. 

Contact XXXXXXXX at [xxxxx@virginia.edu](mailto:xxxxx@virginia.edu) for admin site login information. To get to the live server admin site visit https://solar-tax-webapp.herokuapp.com/admin/ 

The admin site allows us to manually view all instances of any models created by users and allows us to change the parameter values if needed.

### PostgreSQL
This project uses a PostgreSQL database. You will need access to a local database for development and testing and access to the database for the live server.

__PostgreSQL Download__: [https://www.postgresql.org/download/](https://www.postgresql.org/download/).

### Gmail
There is a gmail account for use on this project. 

The sole purpose of this email is to send emails to users for password reset and to send Thomas, Carrie, and Elizabeth emails about feedback received.

## Structure

### SolarTax
The folder holds the Django project. (Only urls.py and settings.py should be changed)

  1. __Settings.py__ - Defines all the Django settings needed for the project. If you install a new dependency, you may have to add it to INSTALLED\_APPS.
  2. __Asgi.py__ - Spins up an instance of the application and uses the settings as defined in the settings.py file.
  3. __Wsgi.py__ - Spins up an instance of the application and uses the settings as defined in the settings.py file. 
  4. __Urls.py__ - Defines the admin URL, URLs that authenticate users which are defined by Django, a URL that makes it possible to display a graph for each project analysis, and then any URL that is defined in the models app.

### Models 
Django application which follows the MVT framework. MVT framework stands for model-view-template. Models are effectively classes that you would find in Java, Python, or C++. Models require certain variables to be defined about them when instantiated. The views take in information from models and request data (&quot;GET&quot; or &quot;POST&quot; methods) and determine what to do with this information. They then pass information to a template. The template is the HTML that defines how to display the information received by the views, although it has a bit more functionality compared to straight HTML as you can pass variables in and use for loops.
  1. __admin.py__ - Tells the admin site to include information about all the models in the project. The admin site allows us to view all data of the project.
  2. __apps.py__ - Defines this app to be named models
  3. __forms.py__ - Defines any forms that are used throughout the project. Most are tied to a model so they can create an instance of a model through a submission of a form. [https://docs.djangoproject.com/en/3.1/topics/forms/](https://docs.djangoproject.com/en/3.1/topics/forms/)
  4. __models.py__ - Defines the UserProfile, Locality, Simulation, and Calculation models. A UserProfile is tied to one Locality, and has many simulations. A Locality can be tied to any number of UserProfiles. A Simulation is only tied to one UserProfile and only has one Calculation model associated with it. A Calculation instance is tied to one Simulation instance. Feedback is a model that holds an email and a text field containing feedback or a question. It is not tied to any other model.
  5. __revenue\_calculations.py__ - Python file that has functions to calculate the revenue for projects based on the input parameters.
  6. __urls.py__ - Defines the URLs that are valid for the web application and which view corresponds to the URL entered.
  7. __views.py__ - Defines the different views needed for the web application. This is the business logic that is needed to get parameters from instances of models or forms and then transform the data if necessary to pass onto the HTML templates to display the web page correctly.
  8. __templates__ - Folder contains the HTML template files that are used when a view calls for a template to display with the necessary parameters. _Base.html_ is a HTML file that contains code that is to be used as a base for the site so all pages have the same basic design. The registration sub-folder contains the templates that are used for the password reset functionality of the web application.
  9. __static__ - Folder contains any images that are displayed on the site and the CSS and JS files used to further design the pages of the web application. Add any new images into this folder and continue to edit the CSS and JS files in this folder if needed.
  10. __templatetags__ - The _custom\_tags.py_ file defines tags that can be used in the HTML templates to manipulate data if necessary from variables that are passed into the templates.

### Other Files
  1. __feedback\_sender.py__ - File is used to send an email to Elizabeth, Carrie, and Thomas at 3pm each weekday, if someone submitted feedback through the web application. This also pings the website 3 times an hour each weekday from 9-5 so the dyno is constantly up in this time period. This means loading times should be faster.
  2. __manage.py__ - Django file that boots the application up when called. Don&#39;t touch unless absolutely necessary.
  3. __Pipfile & Pipfile.lock__ - Files are for the virtual environment and list all the dependencies of the project and the versions used.
  4. __Procfile__ - File that gets the web application running. It runs python manage.py migrate to make any migrations necessary to the database. It then runs the application with the wsgi.py file and finally creates a cron job to run feedback\_sender.py
  5. __requirements.txt__ - File that lists all dependencies is to be used to automatically install all dependencies at once. Keep updated with any new dependencies that are added.
  6. __.gitignore__

## Development
Before running a local server create a new directory named hiddenVars with 3 files named secret_key.txt, email.txt, and email_password.txt. Put the correct variables that can be found on the site into these files. This helps set the correct settings variables for the local server. Also make sure that DEBUG is set to True and ALLOWED_HOSTS = [] before running a local server. DEBUG should be set to False and ALLOWED_HOSTS = ['solar-tax-webapp.herokuapp.com', 'localhost:8000', '127.0.0.1:8000'] for the live server.

For local development make sure you are in the virtual environment you created for the project. Also before running the local server make sure you are located in the same directory as the _manage.py_ file. If you are not, you will not be able to run the local server. Make changes to the project as you see fit, then run your local server using _python manage.py runserver._ Test out the new feature on the local development server and add test cases to tests.py to ensure it does not impact other aspects of the project. Make sure to commit to the github repo consistently on a development branch to ensure progress is saved. Merge to the master branch when appropriate and this will automatically push all updates onto the live server. To make sure the server is created successfully after a change to the master branch is made, visit the project homepage and you will see the project being built and then deployed.
