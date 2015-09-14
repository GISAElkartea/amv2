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

If you want to update the sample data, you can:

```
git checkout sample_data
git rebase origin/master
python manage.py dumpdata --indent 4 --natural-foreign --natural-primary >| sample_data.json
git add sample_data.json
git add -f .media
```

# Running tests

```
python manage.py test
```

# Production

## Checklist

- Tests
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

## Deployment

- Initial beta deploy
- Initial data
- Use and development cycle
- Public release
    - Site name and allowed domains change

