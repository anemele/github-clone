import pytest

from .parser import parse_url, parse_url_batch


def f(url):
    r = parse_url(url)
    if r is None:
        return
    return '/'.join(r)


def test_parse_url_1():
    assert f('x/y') == 'x/y'
    assert f('x/y.git') == 'x/y'
    assert f('https://github.com/x/y') == 'x/y'
    assert f('git@github.com:x/y') == 'x/y'
    assert f('git@github.com:x/y.git') == 'x/y'
    assert f('https://gitbuh.mirror/x/y') == 'x/y'


def test_parse_url_2():
    assert f('xy') is None


@pytest.mark.xfail
def test_parse_url_3():
    # assert f('a/b/c/x/y') == 'x/y'  # how to parse this?
    assert f('https://github.com/x/y/issues') == 'x/y'
    assert f('https://github.com/x/y/releases/tag/v1.0') == 'x/y'


def test_parse_url_batch():
    sample = [
        "xy",
        "x/y",
        "x/y.git",
        "https://github.com/x/y",
        "git@github.com:x/y",
        "https://gitbuh.moc/x/y",
    ]
    expect = [
        # None,
        ('x', 'y'),
        ('x', 'y'),
        ('x', 'y'),
        ('x', 'y'),
        ('x', 'y'),
    ]
    assert list(parse_url_batch(sample)) == expect
