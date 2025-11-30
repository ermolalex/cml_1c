import uuid
from django.db import models
from oscar.apps.catalogue.abstract_models import *

class ProductClass(AbstractProductClass):
    code = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    # def save(self, *args, **kwargs):
    #     if self.ext_id == "":
    #         self.ext_id = uuid.uuid4()
    #     super().save(*args, **kwargs)


"""
class Category(AbstractCategory):
    ext_id = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.ext_id == "":
            self.ext_id = uuid.uuid4()
        super().save(*args, **kwargs)


class ProductAttribute(AbstractProductAttribute):
    ext_id = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.ext_id == "":
            self.ext_id = uuid.uuid4()
        super().save(*args, **kwargs)


class ProductAttributeValue(AbstractProductAttributeValue):
    ext_id = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.ext_id == "":
            self.ext_id = uuid.uuid4()
        super().save(*args, **kwargs)

class AttributeOptionGroup(AbstractAttributeOptionGroup):
    ext_id = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.ext_id == "":
            self.ext_id = uuid.uuid4()
        super().save(*args, **kwargs)

class AttributeOption(AbstractAttributeOption):
    ext_id = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.ext_id == "":
            self.ext_id = uuid.uuid4()
        super().save(*args, **kwargs)

class Product(AbstractProduct):
    ext_id = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    def save(self, *args, **kwargs):
        if self.ext_id == "":
            self.ext_id = uuid.uuid4()
        super().save(*args, **kwargs)


"""

from oscar.apps.catalogue.models import *

# if you wish to customise Oscar’s models, you must declare
#   your custom ones before importing Oscar’s models for that app.
