Django demo with pylabels
=========================

Create an environment, for example

    conda create -n barcode python=3.12

Activate your env

    conda activate barcode

Install Django and tqdm in your environment (DJ 5.1+)

    $ pip install -U Django tqdm

Create a working folder

    mkdir ~/working

Navigate to a working folder

    cd  ~/working

Clone this repo into your working folder

    git clone https://github.com/erikvw/pylabels

Navigate to the root of the pylabels repo

    cd pylabels

and install

    pip install .

Now navigate into the ``pylabels/demos/django_demo/project`` folder

    cd demos/django_demo/project

migrate the database:

    $ python manage.py prepare

Start the test server:

    $ python manage.py runserver

Navigate to:

    http://localhost:8000

The default user is "admin" with password "admin"
