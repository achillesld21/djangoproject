from django.core.files.storage import Storage
from google.cloud import storage as gcs


class GoogleCloudStorage(Storage):
    def __init__(self):
        self.client = gcs.Client()

    def _open(self, name, mode='rb'):
        # Not needed for uploads
        pass

    def _save(self, name, content):
        bucket = self.client.bucket('firstblog')
        blob = bucket.blob(name)
        blob.upload_from_file(content)
        return name

    def delete(self, name):
        bucket = self.client.bucket('firstblog')
        blob = bucket.blob(name)
        blob.delete()

    def exists(self, name):
        bucket = self.client.bucket('firstblog')
        blob = bucket.blob(name)
        return blob.exists()

    def url(self, name):
        # Assuming your bucket is publicly accessible
        return f'https://storage.googleapis.com/firstblog/{name}'