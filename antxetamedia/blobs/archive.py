try:
    from urllib.parse import quote
except ImportError:
    from urllib import quote

from boto.s3.connection import S3Connection, OrdinaryCallingFormat
from boto.s3.bucket import Bucket
from boto.exception import S3CreateError


class ArchiveS3(object):
    def __init__(self, account):
        self.account = account
        # No real connection is maintained open
        self.connection = S3Connection(self.account.username, self.account.password, is_secure=False,
                                       host='s3.us.archive.org', calling_format=OrdinaryCallingFormat())

    def get_bucket_name(self, podcast):
        return '{prefix}-{podcast}'.format(prefix=self.account.username.lower(),
                                           podcast=podcast.slug.lower())[:100]

    def get_bucket_headers(self, podcast, update=False):
        headers = getattr(podcast, 'metadata', {})
        headers = {key: 'uri({})'.format(value) for key, value in headers.items()}
        if update:
            headers['x-archive-ignore-preexisting-bucket'] = 1
        return headers

    def create_or_update_bucket(self, podcast):
        bucket_name = self.get_bucket_name(podcast)
        update = self.connection.lookup(bucket_name) is not None
        headers = self.get_bucket_headers(podcast, update=update)
        try:
            return self.connection.create_bucket(bucket_name, headers=headers)
        except S3CreateError as e:
            if e.status == 409:  # Conflict
                return Bucket(self.connection, bucket_name)
            raise

    def get_key_name(self, blob):
        return str(blob)  # Guaranteed to be unique

    def get_or_create_key(self, blob):
        bucket_name = self.get_bucket_name(blob.content_object)
        bucket = Bucket(self.connection, bucket_name)
        key_name = self.get_key_name(blob)
        key = bucket.get_key(key_name)
        if key is None:
            key = bucket.new_key(key_name)
        return key

    def build_url(self, blob):
        bucket_name = self.get_bucket_name(blob.content_object)
        key_name = self.get_key_name(blob)
        return 'https://archive.org/download/{bucket}/{key}'.format(bucket=quote(bucket_name), key=quote(key_name))
