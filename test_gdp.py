from unittest import TestCase

from gdp import NormalFormat, ShortFormat, KotlinFormat, main


class TestNormalFormat(TestCase):
    def test_parse(self):
        normal_format = NormalFormat()
        deps = normal_format.parse('compile group: \'com.google.firebase\', name: \'firebase-core\', version: \'17.2.1\'')
        assert (deps[0]['type'] == 'compile')
        assert (deps[0]['group'] == 'com.google.firebase')
        assert (deps[0]['name'] == 'firebase-core')
        assert (deps[0]['version'] == '17.2.1')

    def test_format_output(self):
        normal_format = NormalFormat()
        text = normal_format.format_output({'type': 'compile', 'group': 'com.google.firebase', 'name': 'firebase-core', 'version': '17.2.1'})
        self.assertEqual(text, "compile group: 'com.google.firebase', name: 'firebase-core', version: '17.2.1'")


class TestShortFormat(TestCase):
    def test_parse(self):
        short_format = ShortFormat()
        deps = short_format.parse('api \'com.google.firebase:firebase-core:17.2.1\'')
        assert (deps[0]['type'] == 'api')
        assert (deps[0]['group'] == 'com.google.firebase')
        assert (deps[0]['name'] == 'firebase-core')
        assert (deps[0]['version'] == '17.2.1')

    def test_format_output(self):
        short_format = ShortFormat()
        text = short_format.format_output(
            {'type': 'api', 'group': 'com.google.firebase', 'name': 'firebase-core', 'version': '17.2.1'})
        self.assertEqual(text, "api 'com.google.firebase:firebase-core:17.2.1'")


class TestKotlinFormat(TestCase):
    def test_parse(self):
        kotlin_format = KotlinFormat()
        deps = kotlin_format.parse("implementation('com.google.firebase:firebase-core:17.2.1')")
        assert (deps[0]['type'] == 'implementation')
        assert (deps[0]['group'] == 'com.google.firebase')
        assert (deps[0]['name'] == 'firebase-core')
        assert (deps[0]['version'] == '17.2.1')

    def test_format_output(self):
        kotlin_format = KotlinFormat()
        deps = kotlin_format.format_output({'type': 'implementation', 'group': 'com.google.firebase', 'name': 'firebase-core', 'version': '17.2.1'})
        self.assertEqual(deps, "implementation('com.google.firebase:firebase-core:17.2.1')")
