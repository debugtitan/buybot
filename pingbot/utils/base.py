from django.db import models

__all__ = ("BaseModelMixin")

class BaseModelBaseMixin:
    def is_instance_exist(self):
        return self.__class__.objects.filter(id=self.id).exists()

    @property
    def current_instance(self):
        return self.__class__.objects.get(id=self.id)

    @classmethod
    def bulk_create(cls, data: list, *args, **kwargs):
        return cls.objects.bulk_create([cls(**item) for item in data], *args, **kwargs)



class BaseModelMixin(BaseModelBaseMixin, models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_last_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return f"< {type(self).__name__}({self.id}) >"


