
from unittest import TestCase

from pact import translate, Elem


class TestTranslate(TestCase):

    def test_single_child(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon"></i></a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {
            'href': twitter_share,
        },
        Elem(
            'i',
            {
                'class': "fa fa-twitter-square large-icon",
            },
        ),
    )

"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)

    def test_multiple_children(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}>
            <i class="fa fa-twitter-square large-icon"></i>
            <i class="fa fa-facebook-square large-icon"></i>
        </a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {
            'href': twitter_share,
        },
        Elem(
            'i',
            {
                'class': "fa fa-twitter-square large-icon",
            },
        ),
        Elem(
            'i',
            {
                'class': "fa fa-facebook-square large-icon",
            },
        ),
    )

"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)


    def test_empty_tag_translate(self):

        code = """
@pact
def tag(self):
    twitter_share = ""
    return <a href={twitter_share}><i class="fa fa-twitter-square large-icon" /></a>
"""

        expected = """
@pact
def tag(self):
    twitter_share = ""
    return Elem(
        'a',
        {
            'href': twitter_share,
        },
        Elem(
            'i',
            {
                'class': "fa fa-twitter-square large-icon",
            },
        )
    )

"""

        result = translate(code)

        self.assertMultiLineEqual(expected, result)


class TestElem(TestCase):

    def test_empty_elem(self):

        elem = Elem('a', {}, [])

        expected = "<a />"

        self.assertEqual(elem.to_html(), expected)

    def test_elem(self):

        elem = Elem('a', {}, [Elem('b', {}, [])])

        expected = "<a><b /></a>"

        self.assertEqual(elem.to_html(), expected)

    def test_elem_single_attribute(self):

        elem = Elem('a', {'class': 'some-icon'}, [Elem('b', {}, [])])

        expected = '<a class="some-icon"><b /></a>'

        self.assertEqual(elem.to_html(), expected)

    def test_elem_multiple_attribute(self):

        elem = Elem('a', {'class': 'some-icon', 'data-width': 800}, [Elem('b', {}, [])])

        expected = '<a data-width="800" class="some-icon"><b /></a>'

        self.assertEqual(elem.to_html(), expected)
