import sys
import pprint
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from apps.cml import items

# from oscar.core.loading import get_model
#
# Country = get_model("address", "Country")
# Partner = get_model("partner", "Partner")


class Command(BaseCommand):
    help = """Печать файла import.xml в удобочитаемом виде. 
    """
    def handle(self, *args, **options):
        #file_name = Path(settings.CML_UPLOAD_ROOT) / "import.xml"
        file_name = Path(settings.BASE_DIR) / "tests" / "унф" / "import.xml"
        pack = items.Packet.parse(file_name)

        assert pack.version == '2.08'
        #assert pack.create_date.strftime("%Y-%m-%dT%H:%M:%S") == '2025-10-20T12:28:35'

        print(pack.classifier)
        print("*** Groups ***")
        for _ in pack.classifier.groups:
            print(_)
            if len(_.groups) > 0:
                for __ in _.groups:
                    print("--", __)

        print("")
        print("*** Properties ***")
        props = {}
        for prop in pack.classifier.props:
            print(prop)
            #props[prop.uid] = prop.name
            if prop.value_type == items.ValueType.LIST:
                variants = {"Наименование": prop.name, "ТипЗначений": prop.value_type.value}
                for prop_var in prop.variants_list:
                    print("--", prop_var)
                    variants[prop_var.uid] = prop_var.value
                props[prop.uid] = variants
            else:
                props[prop.uid] = {"Наименование": prop.name, "ТипЗначений": prop.value_type.value}

        pprint.pprint(props)

        print("")
        print("*** Categories ***")
        for _ in pack.classifier.categories:
            print(_)

        print("")
        print(pack.catalogue)
        print("")
        for i in range(5):
            print(pack.catalogue.products[i])


"""  Шина Кама
- <ЗначенияСвойств>
- <ЗначенияСвойства>
  <Ид>88e81568-42cd-11f0-9540-00155d58f10a</Ид> 
  <Значение>425</Значение> 
  </ЗначенияСвойства>
- <ЗначенияСвойства>
  <Ид>a46ff8d2-42cd-11f0-9540-00155d58f10a</Ид> 
  <Значение>85</Значение> 
  </ЗначенияСвойства>
- <ЗначенияСвойства>
  <Ид>bf743580-42cd-11f0-9540-00155d58f10a</Ид> 
  <Значение>21</Значение> 
  </ЗначенияСвойства>
- <ЗначенияСвойства>
  <Ид>00258f5c-42ce-11f0-9540-00155d58f10a</Ид> 
  <Значение>18</Значение> 
  </ЗначенияСвойства>
- <ЗначенияСвойства>
  <Ид>222811ba-42ce-11f0-9540-00155d58f10a</Ид> 
  <Значение>2908ce84-42ce-11f0-9540-00155d58f10a</Значение> 
  </ЗначенияСвойства>
- <ЗначенияСвойства>
  <Ид>6d7903cc-42ce-11f0-9540-00155d58f10a</Ид> 
  <Значение>6fe8280e-42ce-11f0-9540-00155d58f10a</Значение> 
  </ЗначенияСвойства>
  </ЗначенияСвойств>

"""


