# SolTax WebApp
This tool is meant for use by Virginia localities to help them decide which taxation model to use for solar generating facilities, either the new Revenue Share model, or the old M&T/Real Estate tax model. The tool allows users to create different analyses of solar projects of various electric capacities and land sizes. It provides a user a detailed analysis of the expected revenues of a solar project under both tax models as well as a total summary of the revenues for all projects under both tax models. 

__SolTax WebApp__: [https://solar-tax-webapp.herokuapp.com/](https://solar-tax-webapp.herokuapp.com/)

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
The admin site allows us to manually view all instances of any models created by users and allows us to change the parameter values if needed. For the live server there is already a superuser created with credentials. Contact Mary Beth Wetherell at [meh4q@virginia.edu](mailto:meh4q@virginia.edu) for admin site login information.

__SolTax WebApp Admin__: https://solar-tax-webapp.herokuapp.com/admin/ 

The local server needs a username and password to access admin site. You will need to create a superuser. To do this type  `_python manage.py createsuperuser_ ` into the command line while in the project directory. Fill out the command line prompts and then to access the admin site run the application using  `_python manage.py runserver_ `, go to [http://localhost:8000/admin](http://localhost:8000/admin) or [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and sign in. 

### PostgreSQL
This project uses a PostgreSQL database. You will need access to a local database for development and testing and access to the database for the live server.

__PostgreSQL Download__: [https://www.postgresql.org/download/](https://www.postgresql.org/download/).

### Gmail
There is a gmail account for use on this project. The sole purpose of this email is to send emails to users for password reset and to send Thomas, Carrie, and Elizabeth emails about feedback received.

## Structure

### SolarTax
The folder holds the Django project. (Only urls.py and settings.py should be changed)

  1. __settings.py__ - Defines all the Django settings needed for the project. If you install a new dependency, you may have to add it to INSTALLED\_APPS.
  2. __asgi.py__ - Spins up an instance of the application and uses the settings as defined in the settings.py file.
  3. __wsgi.py__ - Spins up an instance of the application and uses the settings as defined in the settings.py file. 
  4. __urls.py__ - Defines the admin URL, URLs that authenticate users which are defined by Django, a URL that makes it possible to display a graph for each project analysis, and then any URL that is defined in the models app.

### Models 
Django application which follows the MVT framework. MVT framework stands for model-view-template. Models are effectively classes that you would find in Java, Python, or C++. Models require certain variables to be defined about them when instantiated. The views take in information from models and request data (&quot;GET&quot; or &quot;POST&quot; methods) and determine what to do with this information. They then pass information to a template. The template is the HTML that defines how to display the information received by the views, although it has a bit more functionality compared to straight HTML as you can pass variables in and use for loops.
  1. __admin.py__ - Tells the admin site to include information about all the models in the project. The admin site allows us to view all data of the project.
  2. __apps.py__ - Defines this app to be named models
  3. __forms.py__ - Defines any forms that are used throughout the project. Most are tied to a model so they can create an instance of a model through a submission of a form.
  4. __models.py__ - Defines the UserProfile, Locality, Simulation, and Calculation models. A UserProfile is tied to one Locality, and has many simulations. A Locality can be tied to any number of UserProfiles. A Simulation is only tied to one UserProfile and only has one Calculation model associated with it. A Calculation instance is tied to one Simulation instance. Feedback is a model that holds an email and a text field containing feedback or a question. It is not tied to any other model.
  5. __revenue\_calculations.py__ - Python file that has functions to calculate the revenue for projects based on the input parameters.
  6. __urls.py__ - Defines the URLs that are valid for the web application and which view corresponds to the URL entered.
  7. __views.py__ - Defines the different views needed for the web application. This is the business logic that is needed to get parameters from instances of models or forms and then transform the data if necessary to pass onto the HTML templates to display the web page correctly.
  8. __templates__ - Folder contains the HTML template files that are used when a view calls for a template to display with the necessary parameters. _base.html_ is a HTML file that contains code that is to be used as a base for the site so all pages have the same basic design. The registration sub-folder contains the templates that are used for the password reset functionality of the web application.
  9. __static__ - Folder contains any images that are displayed on the site and the CSS and JS files used to further design the pages of the web application. Add any new images into this folder and continue to edit the CSS and JS files in this folder if needed.
  10. __templatetags__ - The _custom\_tags.py_ file defines tags that can be used in the HTML templates to manipulate data if necessary from variables that are passed into the templates.

### Other Files
  1. __feedback\_sender.py__ - File is used to send an email to Elizabeth, Carrie, and Thomas at 3 PM each weekday, if someone submitted feedback through the web application. This also pings the website 3 times an hour each weekday from 9 AM - 5 PM so the dyno is constantly up in this time period. This means loading times should be faster.
  2. __manage.py__ - Django file that boots the application up when called. Don&#39;t touch unless absolutely necessary.
  3. __Pipfile & Pipfile.lock__ - Files are for the virtual environment and list all the dependencies of the project and the versions used.
  4. __Procfile__ - File that gets the web application running. It runs python manage.py migrate to make any migrations necessary to the database. It then runs the application with the wsgi.py file and finally creates a cron job to run feedback\_sender.py
  5. __requirements.txt__ - File that lists all dependencies is to be used to automatically install all dependencies at once. Keep updated with any new dependencies that are added.
  6. __.gitignore__ - File that tells Git to intentional ignore files that in this case contain sensitive information such as login creditionals which should not be pushed to the repository

## Development
  1. Clone the SolTax repository and create a new branch

    __Working with Github in VS Code Tutorial__:
    
  2. In the terminal