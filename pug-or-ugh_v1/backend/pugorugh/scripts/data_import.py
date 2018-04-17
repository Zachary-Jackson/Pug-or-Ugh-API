# This script is currently working on my windows 8.1 computer, but no
# guarantees about other systems. If this script does not work
# try the old_data_import.py script

import json
import os
import sys

import django

# In order to get the data_import working we need to allow django to
# find the files it needs.

# This means that in order for django to find backend.settings we need
# to go up three folders and put the path in sys.path

# We start in data_import.py, go up to scripts, go to pugorugh then end up
# at the main backend folder.
sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.dirname(
                os.path.abspath(__file__)))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

# Now that django is setup we can import the DogSerializer properly
from pugorugh.serializers import DogSerializer

with open('pugorugh/static/dog_details.json', 'r') as file:
    data = json.load(file)

    serializer = DogSerializer(data=data, many=True)
    if serializer.is_valid():
        serializer.save()
    else:
        print(serializer.errors)
