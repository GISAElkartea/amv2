from django.db.models import BooleanField


class UniqueTrueBooleanField(BooleanField):
    def pre_save(self, model_instance, add):
        value = getattr(model_instance, self.attname)
        if value:
            others = model_instance._default_manager.filter(**{self.attname: True})
            others.update(**{self.attname: False})
        return value
