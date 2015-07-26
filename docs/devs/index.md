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

# Start development server
python manage.py runserver
```

## Sample data

Additionally, if you want some sample data, you can get it by checking out the
`sample_data` branch and loading the `sample_data.json` json file into the
database:

```
python manage.py loaddata sample_data.json
```

You may want to index this data into the search engine with:

```
python manage.py buildwatson
```

To get the media files (images mainly) while working on the `master` branch, you
can checkout the `.media` directory (which is ignored by git by default) from
`sample_data`:

```
git checkout .media -- sample_data
git reset HEAD .media
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
