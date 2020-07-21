# Django
from django.conf import settings
from django.core.files.storage import default_storage

# Storages
from storages.backends.s3boto3 import S3Boto3Storage  # noqa E402


class PublicMediaStorage(S3Boto3Storage):
    location = "media/public"
    default_acl = 'public-read'
    file_overwrite = False


class PrivateMediaStorage(S3Boto3Storage):
    location = 'media/private_media_us'
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


def get_public_media_storage():
    if settings.USE_AWS_S3:
        return PublicMediaStorage()
    else:
        return default_storage


def get_private_media_storage():
    if settings.USE_AWS_S3:
        return PrivateMediaStorage()
    else:
        return default_storage
