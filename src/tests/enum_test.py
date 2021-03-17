from src.app.enum import TextEnum


class TestTextEnum:

    def test_to_string(self):
        class MyEnum(TextEnum):
            FOO = 'my/foo'
            BAR = 'my/bar'

        assert MyEnum.BAR.value == str(MyEnum.BAR) == 'my/bar'

    def test_enumerate_all_values(self):
        class MyEnum(TextEnum):
            FOO = 'my/foo'
            BAR = 'my/bar'
            BAZ = 'my/baz'

        assert MyEnum.values() == (
            'my/foo',
            'my/bar',
            'my/baz'
        )
