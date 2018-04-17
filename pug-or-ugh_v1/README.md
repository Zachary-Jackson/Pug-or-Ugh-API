# Pug or Ugh
This is a website to help pet owners find the dog of their dreams.
The front end of the site will be connected to the database through the Django
REST Framework with proper serialization and models.

This website was built in part with HTML, CSS, and React originally supplied
from www.teamtreehouse.com for a Python Web Development Tech Degree Project.
The HTML, CSS and React is to be considered built by teamtreehouse for this
project, but may be edited by me at some point. The following lines of code in
the README was supplied by teamtreehouse as well.

## Requirements

Create the models, serializers, and views to power the provided Angular
application. You can check through the supplied JavaScript to see what
resources should be available or check below. You are allowed to change,
extend, and improve the JavaScript if desired, but the final result must still
meet all of the required features/abilities.

You've been provided with HTML and CSS for a basic, mobile-friendly design.
You've also been provided with a starter Django project and application, a
serializer and views for authentication, and a bit more.

## Starting

Create a virtualenv and install the project requirements, which are listed in
`requirements.txt`. The easiest way to do this is with `pip install -r
requirements.txt` while your virtualenv is activated.

After this initialize the database with python manage.py migrate. You are then
able to run the `data_import.py` script to import all of the dog models into
the database if desired. If data_import.py does not work try the
`old_data_import` script that came with the project. The data_import script
works on Windows 8.1, but I am not sure about the old_data_import script.

## Models

The following models and associated field names should be present as they
will be expected by the JavaScript application.

* `Dog` - This model represents a dog in the app.

	Fields:

	* `name`
	* `image_filename`
	* `breed`
	* `age`, integer for months
	* `gender`, "m" for male, "f" for female, "u" for unknown
	* `size`, "s" for small, "m" for medium, "l" for large, "xl" for extra
	  large, "u" for unknown

* `UserDog` -  This model represents a link between a user an a dog

	Fields:

	* `user`
	* `dog`
	* `status`, "l" for liked, "d" for disliked

* `UserPref` - This model contains the user's preferences

	Fields:

	* `user`
	* `age`, "b" for baby, "y" for young, "a" for adult, "s" for senior
	* `gender`, "m" for male, "f" for female
	* `size`, "s" for small, "m" for medium, "l" for large, "xl" for extra
	  large

	`age`, `gender`, and `size` can contain multiple, comma-separated values

## Serializers

You'll need to provide serializers for both the `Dog` and `UserPref` models.
Each of them should reveal all of the fields with one exception: the `UserPref`
serializer doesn't need to reveal the user.

## Routes

The following routes are expected by the JavaScript application.

* To get the next liked/disliked/undecided dog

	* `/api/dog/<pk>/liked/next/`
	* `/api/dog/<pk>/disliked/next/`
	* `/api/dog/<pk>/undecided/next/`

* To change the dog's status

	* `/api/dog/<pk>/liked/`
	* `/api/dog/<pk>/disliked/`
	* `/api/dog/<pk>/undecided/`

* To change or set user preferences

	* `/api/user/preferences/`
