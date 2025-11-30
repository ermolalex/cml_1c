import uuid
from django.db import models

from oscar.apps.catalogue.abstract_models import AbstractProductClass

class ProductClass(AbstractProductClass):
    code = models.CharField(max_length=36, db_index=True, unique=True, blank=True, editable=False)

    # def save(self, *args, **kwargs):
    #     if self.ext_id == "":
    #         self.ext_id = uuid.uuid4()
    #     super().save(*args, **kwargs)

from oscar.apps.catalogue.models import *
