# Django Project Setup with MySQL Database

This guide will walk you through the steps to set up and configure a Django project with a MySQL database using the files in the `Athelet Tracking System.rar` archive. Follow the instructions below to get your Django project up and running.

## Prerequisites

- Python 3.x installed on your system
- MySQL database server installed
- Extraction tool like 7-Zip or WinRAR
- A command-line interface (CLI) or terminal

## Step 1: Extract the `.rar` File

1. Use a tool like [7-Zip](https://www.7-zip.org/), [WinRAR](https://www.win-rar.com/), or [Unarchiver](https://theunarchiver.com/) to extract `Athelet Tracking System.rar`.
2. Note the location where you extracted the files, as this will be your project directory.

## Step 2: Install Django and Required Packages

1. Open a command prompt or terminal and navigate to your project directory.
2. Install all the necessary packages using the `requirements.txt` file by running the following command:

    ```bash
    pip install -r requirements.txt
    ```

## Step 3: Install MySQL

1. Download MySQL from the [official website](https://dev.mysql.com/downloads/mysql/).
2. Follow the installation prompts and note the username and password you create during the setup.

## Step 4: Configure MySQL for Django

1. Access the MySQL command line or use a graphical tool

## Step 5: Configure Django Settings

1. Open the `settings.py` file in your Django project directory.
2. Replace the existing database settings with the following configuration:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'django_db',
            'USER': 'django_user',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '3306',
        }
    }
    ```

## Step 6: Make and Run Migrations

1. Prepare the database migrations by running:

    ```bash
    python manage.py makemigrations
    ```

2. Apply the migrations to create or update the database tables:

    ```bash
    python manage.py migrate
    ```

## Step 7: Create a Superuser

1. To access the Django admin interface, create a superuser by running the command:

    ```bash
    python manage.py createsuperuser
    ```

2. Follow the prompts to enter your username, email, and password.

## Step 8: Run the Django Server

1. Start the Django development server by running:

    ```bash
    python manage.py runserver
    ```

2. Open your web browser and go to `http://127.0.0.1:8000/` to view your Django site.

## Conclusion

You have successfully set up a Django project with a MySQL database using the `Athelet Tracking System.rar` file. For further development and customization, refer to the Django documentation and MySQL resources.



