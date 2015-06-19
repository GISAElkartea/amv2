Development
-----------

    # Install python dependencies
    pip install -r requirements.txt

    # Install javascript dependencies
    cd antxetamedia/static
    bower install
    cd ../..

    # Setup the database
    python manage.py migrate

    # Start development server
    python manage.py runserver
