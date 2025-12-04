import uuid
from django.db import models

from oscar.apps.catalogue.abstract_models import AbstractProductClass, AbstractProduct, AbstractCategory

class ProductClass(AbstractProductClass):
    c1_uid = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    # def save(self, *args, **kwargs):
    #     if self.ext_id == "":
    #         self.ext_id = uuid.uuid4()
    #     super().save(*args, **kwargs)

class Product(AbstractProduct):
    c1_uid = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)


class Category(AbstractCategory):
    c1_uid = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)


from oscar.apps.catalogue.models import *
