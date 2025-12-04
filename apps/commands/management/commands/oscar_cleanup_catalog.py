import logging
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from oscar.core.loading import get_model

Category = get_model("catalogue", "Category")
ProductClass = get_model("catalogue", "ProductClass")
#Partner = get_model("partner", "Partner")

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = """Печать файла import.xml в удобочитаемом виде. 
    """
    def handle(self, *args, **options):

        yes_no = input("Вы уверены, что хотите удалить каталог товаров? (y/n):")

        if yes_no != "y":
            logger.info("Ничего не удалено")
            return

        Category.objects.all().delete()
        logger.info("Группы товаров удалены")

        ProductClass.objects.all().delete()
        logger.info("Категории товаров удалены")
