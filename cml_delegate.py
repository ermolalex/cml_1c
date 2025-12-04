# -*- coding: utf-8 -
"""
This file was generated with the cml_init management command.
It contains UserDelegate class with methods for import one CML packet.
All you need is implement these methods.

All data structures explained in `cml.items` module.
"""
import logging

# Some libraries you may need also
from django.core.exceptions import ObjectDoesNotExist
from oscar.core.loading import get_model

from apps.catalogue.models import Product as TypeProduct
from apps.cml import utils, items
from utils.str_utils import slugify


logger = logging.getLogger(__name__)

Category = get_model("catalogue", "Category")
ProductClass = get_model("catalogue", "ProductClass")
Product: TypeProduct = get_model("catalogue", "Product")


class UserDelegate(utils.AbstractUserDelegate):
    """This object is created every time, when new xml CML packet imports"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore

        # Example of statistics
        self.c_add_prod_classes = 0
        self.c_add_categories = 0
        self.c_del_img = 0
        self.c_saved_img = 0

    def get_report(self) -> str:
        """Report a custom message for finished process"""
        return f"""OK:
               del_img={self.c_del_img}
               saved_img={self.c_saved_img}
               add_prod_classes={self.c_add_prod_classes}
               add_categories={self.c_add_categories}"""



    def _import_groups(self, groups: [items.Group]):  # cml.Group = oscar.Category
        if len(groups) == 0:
            logger.info("Пустой список Групп. Ничего не загружаем.")
            return

        for item in groups:
            try:
                # проверяем, нет ли уже такой группы
                root = Category.objects.get(c1_uid=item.uid)
            except ObjectDoesNotExist:
                # если нет, то создаем, но специальным методом из модуля django-treebeard
                root = Category.add_root(
                    name=item.name,
                    c1_uid=item.uid,
                    slug=slugify(item.name),
                    description="Описание",
                    long_description="Длинное описание",
                    # image = models.ImageField(
                    #     _("Image"), upload_to="categories", blank=True, null=True, max_length=255
                    # )
                    is_public=True,
                )
                self.c_add_categories += 1

            #todo так работает только для 2-х уровневой иерархии. переделать
            for child in item.groups:
                try:
                    # проверяем, нет ли уже такой группы
                    _ = Category.objects.get(c1_uid=child.uid)
                except ObjectDoesNotExist:
                    # если нет, то создаем, но специальным методом из модуля django-treebeard
                    root.add_child(name=child.name, c1_uid=child.uid)
                    self.c_add_categories += 1


    def _import_product_classes(self, categories: [items.Category]):  # cml.Category = oscar.ProductClass (or ProductType)
        if len(categories) == 0:
            logger.info("Пустой список Категорий. Ничего не загружаем.")
            return

        for item in categories:
            try:
                # проверяем, нет ли уже такой категории
                cat = ProductClass.objects.get(c1_uid=item.uid)
            except ObjectDoesNotExist:
                # если нет, то создаем
                product_class = ProductClass(
                    name=item.name,
                    c1_uid=item.uid,
                    requires_shipping=True,  # todo  добавить в 1С?
                    track_stock=True,  # todo  добавить в 1С?
                )
                product_class.save()
                self.c_add_prod_classes += 1


    def import_classifier(self, item: items.Classifier):
        """update_or_create groups, predefined fields"""
        self._import_groups(item.groups)
        self._import_product_classes(item.categories)

        print(self.get_report())


    def _import_catalogue(self, catalog: items.Catalogue):
        """update_or_create products from catalogue, delete all others if need"""
        for item in catalog.products:
            try:
                # проверяем, нет ли уже такого товара
                product = Product.objects.get(c1_uid=item.uid)
            except ObjectDoesNotExist:
                # если нет, то создаем
                category = Category.objects.get(c1_uid=item.group_uids)
                product = Product(
                    c1_uid=item.uid,
                    # structure: default=STANDALONE
                    # is_public: default=True
                    title=item.name,
                    slug=slugify(item.name),
                    description=item.desc,
                    #priority: default=0, "The highest priority products are shown first"
                    ca

                )
                product.save()
                self.c_add_prod_classes += 1


        print(catalog)

        # Update statistics:
        # self.c_del_img += 1
        # self.c_saved_img += 1

    def import_offers(self, off_pack: items.OffersPack):
        """update_or_create prices of loaded products from catalogue"""
        pass

    def import_document(self, doc: items.Document):
        """Import document such an order or delivery. See doc.doc_type"""
        pass

    def export_orders(self) -> [items.Document]:
        """Create documents-orders for sending back. """
        pass
