# -*- coding: utf-8 -
"""
This file was generated with the cml_init management command.
It contains UserDelegate class with methods for import one CML packet.
All you need is implement these methods.

All data structures explained in `cml.items` module.
"""
from decimal import Decimal as D
import logging
from itertools import product

# Some libraries you may need also
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from oscar.core.loading import get_model, get_class

from apps.catalogue.models import Product as TypeProduct
from apps.cml import utils, items
from utils.str_utils import slugify


logger = logging.getLogger(__name__)

Category = get_model("catalogue", "Category")
ProductClass = get_model("catalogue", "ProductClass")
ProductCategory = get_model("catalogue", "ProductCategory")
Product = get_model("catalogue", "Product")
StockRecord = get_model("partner", "StockRecord")
Partner = get_model("partner", "Partner")

create_from_breadcrumbs = get_class("catalogue.categories", "create_from_breadcrumbs")



class UserDelegate(utils.AbstractUserDelegate):
    """This object is created every time, when new xml CML packet imports"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # type: ignore

        # Example of statistics
        self.c_add_prod_classes = 0
        self.c_add_categories = 0
        self.c_add_products = 0
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

        def _handle_node(groups: [items.Group], parent: items.Group = None):
            for group in groups:
                try:
                    cat = Category.objects.get(c1_uid=group.uid)
                except Category.DoesNotExist:
                    if not parent:  # группа верхнего уровня
                        cat = Category.add_root(name=group.name)
                    else:
                        cat = parent.add_child(name=group.name)

                    cat.c1_uid = group.uid
                    # todo этих полей нет XML !
                    # category.description="Описание"
                    # category.long_description="Длинное описание"
                    # category.image = file_path

                    cat.save()
                    self.c_add_categories += 1

                _handle_node(group.groups, cat)



        _handle_node(groups)
        logger.info(f"Обработано групп: {self.c_add_categories}")


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


    def import_catalogue(self, catalog: items.Catalogue):
        for item in catalog.products:
            # ProductClass (Категория  в xml)
            try:
                product_class = ProductClass.objects.get(c1_uid=item.category_uid)
            except ProductClass.DoesNotExist:
                logger.warning(f"В базе не найден класс товаров (Категория  в xml) с кодом: {item.uid}")
                continue

            product_category = None
            if len(item.group_uids) > 0:  # нету категории (Группы в XML)
                try:
                    product_category = Category.objects.get(c1_uid=item.group_uids[0])  # todo может быть несколько групп
                except ProductClass.DoesNotExist:
                    logger.warning(f"В базе не найдена категория товаров (Группа  в xml) с кодом: {tem.group_uids[0]}")

            product, created = Product.objects.get_or_create(c1_uid=item.uid)
            if created: self.c_add_products += 1

            product.title = item.name
            product.slug = slugify(item.name)
            product.description = item.desc
            product.product_class = product_class
            product.code = item.code  # "Код товара" в 1С
            product.c1_uid = item.uid

            product.save()  # todo не подойдет ли тут bulk_upsert

            # Category
            if product_category:
                ProductCategory.objects.update_or_create(product=product, category=product_category)

        # Update statistics:
        # self.c_del_img += 1
        # self.c_saved_img += 1

    def import_offers(self, off_pack: items.OffersPack):
        offers = off_pack.offers
        partner = Partner.objects.get(name=settings.OSCAR_FULFILMENT_PARTNER_NAME)

        for c, offer in enumerate(offers):
            try:
                product = Product.objects.get(c1_uid=offer.product_uid)
            except Product.DoesNotExist:
                logger.info(f"При разборе оффера #{c} не найден товар с uid {offer.product_uid}")
                continue

            try:
                stock = StockRecord.objects.get(partner_sku=offer.product_uid)
            except StockRecord.DoesNotExist:
                stock = StockRecord()

            # todo
            stock_count = int(offer.stock_count)
            if stock_count < 0:
                stock_count = 10

            stock.product = product
            stock.partner = partner
            stock.partner_sku = offer.product_uid
            stock.price = D(offer.prices[0].price)
            stock.num_in_stock = stock_count
            stock.save()

    def import_document(self, doc: items.Document):
        """Import document such an order or delivery. See doc.doc_type"""
        pass

    def export_orders(self) -> [items.Document]:
        """Create documents-orders for sending back. """
        pass

"""
#Create or get a ProductClass
from oscar.core.utils import create_from_breadcrumbs
from oscar.core.models import ProductClass
from oscar.core.models import Product
from oscar.core.models import ProductCategory


product_class, _ = ProductClass.objects.get_or_create(name='Some Product Type')

category_string = create_from_breadcrumbs('main>sub>deeper')

product, _ = Product.objects.get_or_create(
    upc='some_unique_upc',
    defaults={
        'title': 'My Awesome Product',
        'product_class': product_class
    }
)

ProductCategory.objects.update_or_create(
    product=product,
    category=category_string
)

"""