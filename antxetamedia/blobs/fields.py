from django.contrib.contenttypes.models import ContentType

from .models import Blob


class RelatedBlobField(object):
    def __get__(self, instance, owner):
        if instance is None:
            return super(RelatedBlobField, self).__get__(instance, owner)
        ctype = ContentType.objects.get_for_model(instance)
        return Blob.objects.get(content_type=ctype, object_id=instance.pk)

    def __set__(self, instance, value):
        value.content_object = instance
        value.save()

    def __delete__(self, instance):
        ctype = ContentType.objects.get_for_model(instance)
        Blob.objects.filter(content_type=ctype, object_id=instance.pk).delete()
