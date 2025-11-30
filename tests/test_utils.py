from utils.slugify import slugify

def test_slugify():
    assert slugify("молоко") == "moloko"
    assert slugify("молоко-21") == "moloko-21"
    assert slugify("молоко_21") == "moloko_21"
    assert slugify("молоко:#$%&*(()*&^21") == "moloko21"
    assert slugify("молоко 21") == "moloko-21"

    assert slugify("молоко -21", no_minus=True, no_space=True) == "moloko__21"
