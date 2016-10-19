from . import *
from dementia import *
from time import sleep


def test_create():
    assert_raises(AssertionError, Dementia, max_len=1, max_age_seconds=-1)
    assert_raises(AssertionError, Dementia, max_len=0, max_age_seconds=1)

    d = Dementia(max_len=3, max_age_seconds=0.01)
    eq_(len(d), 0)


def test_basics():
    d = Dementia(max_len=3, max_age_seconds=0.01, pool_time=100)

    eq_(d.get('a'), None)
    d['a'] = 'x'
    eq_(d.get('a'), 'x')

    sleep(0.01)
    eq_(d.get('a'), None)

    d['a'] = 'y'
    eq_(d.get('a'), 'y')

    ok_('b' not in d)
    d['b'] = 'y'
    ok_('b' in d)

    sleep(0.01)
    ok_('b' not in d)

    # a is still in Dementia, next values should expire it
    d['c'] = 'x'
    d['d'] = 'y'
    d['e'] = 'z'

    # dict if full
    ok_('c' in d)
    ok_('d' in d)

    d['f'] = '1'
    # c should gone after that
    ok_('c' not in d, 'Len of dict is more than max_len')

    # test __delitem__
    del d['e']
    ok_('e' not in d)


def test_pop():
    d = Dementia(max_len=3, max_age_seconds=0.01)
    d['a'] = 'x'
    eq_('x', d.pop('a'))
    sleep(0.01)
    eq_(None, d.pop('a'))


def test_repr():
    d = Dementia(max_len=2, max_age_seconds=0.01)
    d['a'] = 'x'
    eq_(str(d), "Dementia([('a', 'x')])")
    sleep(0.01)
    eq_(str(d), "Dementia([])")


def test_iter():
    d = Dementia(max_len=10, max_age_seconds=0.01, pool_time=100)
    eq_([k for k in d], [])
    d['a'] = 'x'
    d['b'] = 'y'
    d['c'] = 'z'
    eq_([k for k in d], ['a', 'b', 'c'])

    eq_([k for k in d.values()], ['x', 'y', 'z'])
    sleep(0.01)
    eq_([k for k in d.values()], [])


def test_clear():
    d = Dementia(max_len=10, max_age_seconds=10)
    d['a'] = 'x'
    eq_(len(d), 1)
    d.clear()
    eq_(len(d), 0)


def test_setdefault():
    d = Dementia(max_len=10, max_age_seconds=0.01)

    eq_('x', d.setdefault('a', 'x'))
    eq_('x', d.setdefault('a', 'y'))

    sleep(0.01)

    eq_('y', d.setdefault('a', 'y'))

def test_time_reset():
    d = Dementia(max_len=1, max_age_seconds=20, pool_time=10)
    d['a'] = 'x'
    sleep(1.05)
    _ = d.__getitem__('a', with_age=False)
    _, age = d.__getitem__('a', with_age=True)
    ok_(age < 1.0)

def test_expired():
    d = Dementia(max_len=1, max_age_seconds=2, pool_time=1)
    d['a'] = 'x'
    sleep(2.00)
    ok_('a' not in d)


def test_not_implemented():
    d = Dementia(max_len=10, max_age_seconds=10)
    assert_raises(NotImplementedError, d.fromkeys)
    assert_raises(NotImplementedError, d.iteritems)
    assert_raises(NotImplementedError, d.itervalues)
    assert_raises(NotImplementedError, d.viewitems)
    assert_raises(NotImplementedError, d.viewkeys)
    assert_raises(NotImplementedError, d.viewvalues)
