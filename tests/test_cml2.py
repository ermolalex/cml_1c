from cml import items

def test_read_pack():
    pack = items.Packet.parse("import.xml")

    assert pack.version == '2.08'
    assert pack.create_date.strftime("%Y-%m-%dT%H:%M:%S") == '2025-10-20T12:28:35'

    print(pack.classifier)
    print("")
    for _ in pack.classifier.groups:
        print(_)
        if len(_.groups) > 0:
            for __ in _.groups:
                print("--", __)

    print("")
    print(pack.catalogue)
    print("")
    for i in range(5):
        print(pack.catalogue.products[i])





