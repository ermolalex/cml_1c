from lxml import etree

some_xml = """
<КоммерческаяИнформация xmlns="urn:1C.ru:commerceml_210" xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" ВерсияСхемы="2.08" ДатаФормирования="2025-10-20T12:28:35">
	<Классификатор>
		<Ид>5d1d1996-e373-4a5f-ae0d-1494ca033024</Ид>
		<Наименование>Классификатор (Каталог 2025.10.20 12:06:14)</Наименование>
		<Владелец>
			<Ид>e01f973b-0965-11f0-940a-fa163e4f2bb2</Ид>
			<Наименование>Орлюк Кристина Сергеевна</Наименование>
			<ИНН>780244264216</ИНН>
			<ПолноеНаименование>Индивидуальный предприниматель Орлюк Кристина Сергеевна</ПолноеНаименование>
		</Владелец>
		<!-- some comment -->
		<Группы>
			<Группа>
				<Ид>c4dde1b0-c360-11ef-8083-fa163e4f2bb2</Ид>
				<Наименование>Сыродавленная продукция</Наименование>
			</Группа>
        </Группы>
    </Классификатор>
</КоммерческаяИнформация>
"""

def test_root_creation():
    root = etree.Element("root")

    assert root.tag == "root"


def test_parsing_from_string():
    root = etree.fromstring(some_xml)

    assert "КоммерческаяИнформация" in root.tag


def test_parsing_file():
    tree = etree.parse("import.xml")
    root = tree.getroot()

    assert "КоммерческаяИнформация" in root.tag


def test_element_iter():
    root = etree.fromstring(some_xml)

    for elem in root.iter("*"):
        print(elem)

    assert True


def test_remove_namespace():
    root = etree.fromstring(some_xml)

    for elem in root.iter("*"):
        # пропускаем комментарии
        if (
            isinstance(elem, etree._Comment)
            or isinstance(elem, etree._ProcessingInstruction)
        ):
            continue

        elem_name = etree.QName(elem).localname
        print(elem_name)

        if "urn:1C.ru:commerceml_210" in elem_name:
            assert False

    assert True