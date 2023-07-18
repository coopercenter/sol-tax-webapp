# SolTax WebApp
This tool is meant for use by Virginia localities to help them decide which taxation strategy to use for solar generating facilities, either the new Revenue Share ordinance or the old M&T/Real Estate tax strategy. The tool allows users to create different analyses of solar projects of various electric capacities and land sizes. It provides a user a detailed analysis of the expected revenues of a solar project under both tax options as well as a total summary of the revenues for all projects under both tax options. 

__SolTax WebApp__: [https://solar-tax-webapp.azurewebsites.net/](https://solar-tax-webapp.azurewebsites.net/)

## Sections
1. [Getting Started](#getting-started)
2. [Structure](#structure)
3. [Development](#development)
3. [Debugging Tips](#debugging-tips)

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

### Azure
SolTax and its PostgreSQL database are hosted on Azure which is a cloud computing platform run by Microsoft. When commit changes are pushed onto the master branch, it is deployed directly to Azure. The PostgreSQL database on be viewed through the admin site or Navicat. For Navicat login information, contact Mary Beth Wetherell at [meh4q@virginia.edu](mailto:meh4q@virginia.edu).

### Admin Site
The admin site allows us to manually view all instances of any models created by users and allows us to change the parameter values if needed. For the live server there is already a superuser created with credentials. For admin site login information, contact Mary Beth Wetherell at [meh4q@virginia.edu](mailto:meh4q@virginia.edu).

__SolTax WebApp Admin__: https://solar-tax-webapp.azurewebsites.net/admin/ 

The local server needs a username and password to access admin site. You will need to create a superuser. To do this type  `_python manage.py createsuperuser_ ` into the command line while in the project directory. Fill out the command line prompts and then to access the admin site run the application using  `_python manage.py runserver_ `, go to [http://localhost:8000/admin](http://localhost:8000/admin) or [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and sign in. 

### PostgreSQL
This project uses a PostgreSQL database which holds information on localites and users. You will need access to the Azure database for development and testing. For Azure database credentials information, contact Mary Beth Wetherell at [meh4q@virginia.edu](mailto:meh4q@virginia.edu).

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
  4. __Procfile__ - File that gets the web application running. It runs python manage.py migrate to make any migrations necessary to the database. It then runs the application with the _wsgi.py file_ and finally creates a cron job to run _feedback\_sender.py_
  5. __requirements.txt__ - File that lists all dependencies is to be used to automatically install all dependencies at once. Keep updated with any new dependencies that are added.
  6. __.gitignore__ - File that tells Git to intentional ignore files that in this case contain sensitive information such as login creditionals which should not be pushed to the repository

## Development
1. Clone the SolTax repository and create a new branch for development

    __Working with Github in VS Code Tutorial__: [https://docs.djangoproject.com/en/3.1/intro/tutorial01/](https://docs.djangoproject.com/en/3.1/intro/tutorial01/)

2. In the command line, run `pip install -r requirements.txt` to download the necessary packages
3. Create _.txt_ files containing the following names and respective contents under a new _hiddenVars_ folder in the base directory. The file contains sensitive information that should not be shared. The contents may be found on Azure under _Settings_ :arrow_right: _Configuration_ :arrow_right: _Application settings_. Otherwise, contact Mary Beth Wetherell at [meh4q@virginia.edu](mailto:meh4q@virginia.edu) for sensitive information.
 
| Variable | Description | Example |
| ------------- | ------------- | ------------- |
| azure_host | URL of database | soltax.postgres.database.azure.com |
| azure_name | Name of database | SolTax |
| azure_password | Account Password to access database | password123 |
| azure_port | Port of database | 4321 |
| azure_user  | Account Username to access database | soltaxuser |
| email | Email Username used for SolTax feedback | soltax@gmail.com |
| email_password | Email Password used for SolTax feedback | password123 |
| secret_key | Key used to encrypt sensitive information | asdfh(#*faks(#4nkd)32n3*#nj |

4. Connect to _UVA Anywhere_ VPN
5. In the command line, run `python manage.py runserver`. Ensure that your command line is in the same directory as _manage.py_. 
    - If the command is successful, SolTax should be running on your local server at [https://localhost8000](https://localhost8000) or [http://127.0.0.1:8000](http://127.0.0.1:8000). 
    - Otherwise, address the runtime error as needed and run the command again. For additional help, see [Debugging Tips](#debugging-tips). 
6. Make the additional needed changes to SolTax while running the server perodically to ensure the changes made are successful
7. When all needed changes have been made and the local server runs successfully, push all your changes to the _dev_ branch. If using Git, in the command line, run `git add file_name` to add the file(s) that have been changed. Next, in the command line, run `git commit 'commit_name'` to name your commit and run `push origin -u dev` to push your changes to the _dev_ branch.
8. The _dev_ branch deploys to a SolTax Developer webapp which includes the preloaded configurations used by SolTax to test your changes on the Azure server. If changes are needed for the preloaded configurations, contact Mary Beth Wetherell at [meh4q@virginia.edu](mailto:meh4q@virginia.edu) for access. Changes pushed to the _dev_ branch will automatically be deployed to the developer webapp and can be tracked in the _Actions_ tab on Github.

    __SolTax Developer WebApp__: [https://solar-tax-webapp-dev.azurewebsites.net](https://solar-tax-webapp-dev.azurewebsites.net)

9. After checking to ensure the developer Azure site is successful, merge your branch with the master branch to update the SolTax webapp. Otherwise, if the deployment failed or the server failed to load, address the error as needed, push the changes to your branch, and redeploy the code. For additional help, see [Debugging Tips](#debugging-tips). 

## Debugging Tips

### Deprecated Packages
1. Deprecated packages are outdated past their newest version and should be updated as it may pose both a security risk and result in runtime errors. The runtime error displayed will likely point to the packages that are needing to be updated. 
2. Updating deprecated packages may require changing `import` statements, adding new lines of code in accordance with the documentation of the newest iteration often made in _settings.py_, or changing the version in _requirements.txt_ as indicated after the `==`.

### Package Dependencies
1. As packages are updated, this often results in runtime errors as packages often call on each other and therefore rely on certain versions of a particular package. Therefore, _requirement.txt_ must outline packages that include the correct version of each package's dependencies in order to be successfully deployed.The runtime error displayed will likely outline the package's missing dependencies and their necessary versions.
2. Changing package dependencies is a process of repeated trial and error, involving deprecating as needed after the `==` or changing the order of packages in  _requirement.txt_ to be successful. While the packages may run successfully on your computer, there will likely be errors when deploying on Azure as their operating systems differ. 

### Deployment Failure
1. The error can be found by checking the deployment logs and clicking on the commit ID that was deployed or on the repoistory under actions in the respective workflow.
2. As your computer's operating system likely differs from Azure, the error is likely from the result of a failure in [Package Dependencies](#package-dependencies). 
3. If package dependencies cannot be reconciled, a potential solution is to dockerize the web app by placing it with your computer's operation system but the current iteration of the web app is not dockerized. 

 ### Runtime Errors
 1. If the developer web app or local server displays an error, additional information can be found by setting `DEBUG = TRUE` in _settings.py_ but __must__ set back to `DEBUG = FALSE` before merging your branch with the master branch.
 2. The error is likely the result of [Deprecated Packages](#deprecataed-packages) or updating the code as needed to with the newest iteration of Django.