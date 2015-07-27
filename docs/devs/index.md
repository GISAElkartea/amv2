# Development setup

```
# Install python dependencies
pip install -r requirements.txt

# Install javascript dependencies
cd antxetamedia/static
bower install
cd ../..

# Setup the database
python manage.py migrate

# Compile messages
python manage.py compilemessages

# Start development server
python manage.py runserver
```

## Sample data

Additionally, if you want some sample data, you can import it from the
`sample_data` branch:

```
git checkout sample_data -- sample_data.json .media
git reset HEAD
```

Then you can load it into the database:

```
python manage.py loaddata sample_data.json
```

You may want to index this data into the search engine too:

```
python manage.py buildwatson
```

# Running tests

```
python manage.py test
```

# Production

## Checklist

- Database
- Security
- I18N
- Static files
- Media files
- Logging
- Error reporting
- Initial data
- Stats
- User docs
- CI
- Site
- Groups
- Users
