# -*- coding: utf-8 -*-
import sys

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from oscar.core.loading import get_model

Country = get_model("address", "Country")
Partner = get_model("partner", "Partner")


class Command(BaseCommand):
    help = """Populates the initial data: 
    - list of countries with data from pycountry,
    - first fulfilment partner"""
    

    def handle(self, *args, **options):
        try:
            import pycountry
        except ImportError:
            raise CommandError(
                "You are missing the pycountry library. Install it with "
                "'pip install pycountry'"
            )

        if Country.objects.exists():
            # exit quietly, as the initial load already seems to have happened.
            self.stdout.write("Countries already populated; nothing to be done.")
        else:
            countries = [
                Country(
                    iso_3166_1_a2=country.alpha_2,
                    iso_3166_1_a3=country.alpha_3,
                    iso_3166_1_numeric=country.numeric,
                    printable_name=country.name,
                    name=getattr(country, "official_name", ""),
                    is_shipping_country=True,
                )
                for country in pycountry.countries if country.alpha_2 in settings.OSCAR_SHIPPING_COUNTRIES
            ]

            Country.objects.bulk_create(countries)
            self.stdout.write("Successfully added %s countries." % len(countries))  #todo все сообщения! перенести в log

        if Partner.objects.exists():
            self.stdout.write("Fulfilment partner already populated; nothing to be done.")
        else:
            partner = Partner(name=settings.OSCAR_FULFILMENT_PARTNER_NAME)
            partner.save()
            self.stdout.write("Successfully added fulfilment partner.")
