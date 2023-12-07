from .parser import parse_url, parse_url_batch


def f(url):
    r = parse_url(url)
    if r is None:
        return
    return '/'.join(r)


def test_parse_url_1():
    assert f('x/y') == 'x/y'
    assert f('x/y.git') == 'x/y'
    assert f('/x/y') == 'x/y'
    assert f('/x/y.git') == 'x/y'    
    assert f('https://github.com/x/y') == 'x/y'
    assert f('https://github.com/x/y.git') == 'x/y'
    assert f('git@github.com:x/y') == 'x/y'
    assert f('git@github.com:x/y.git') == 'x/y'
    assert f('https://github.mirror/x/y') == 'x/y'
    assert f('https://github.mirror/x/y.git') == 'x/y'
    assert f('https://a.b.c/x/y') == 'x/y'
    assert f('https://a.b.c/x/y.git') == 'x/y'

    assert f('a-b/c_d') == 'a-b/c_d'
    assert f('a-b/c_d.git') == 'a-b/c_d'
    assert f('a-b/c_d.git.git') == 'a-b/c_d.git'
    assert f('a-b/c_d.github.io') == 'a-b/c_d.github.io'
    assert f('a-b/c_d.github.io.git') == 'a-b/c_d.github.io'
    assert f('a-b/c_d.github.io.git.git') == 'a-b/c_d.github.io.git'


def test_parse_url_2():
    assert f('xy') is None
    assert f('https://github.com/xy') is None


def test_parse_url_3():
    assert f('a/b/c/x/y') == 'a/b'
    assert f('a/b.git/c/x/y') == 'a/b.git'
    assert f('a/b/c/x/y.git') == 'a/b'
    assert f('a/b.git/c/x/y.git') == 'a/b.git'
    assert f('a/b.git/c.git/x.git/y.git') == 'a/b.git'
    assert f('/a/b.git/c.git/x.git/y.git') == 'a/b.git'

    assert f('https://github.com/x/y/issues') == 'x/y'
    assert f('https://github.com/x/y.git/issues') == 'x/y.git'
    assert f('https://github.com/x/y/issues.git') == 'x/y'
    assert f('https://github.com/x/y.git/issues.git') == 'x/y.git'

    assert f('https://github.com/x/y/releases/tag/v1.0') == 'x/y'
    assert f('https://github.com/x/y.git/releases/tag/v1.0') == 'x/y.git'
    assert f('https://github.com/x/y/releases/tag/v1.0.git') == 'x/y'


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
