# coding: utf-8

from datetime import datetime, date, timedelta

import pytest

import jzqt.timetools as jt


class TestTimerange(object):

    def test_init_raise_value_error(self):
        msg = 'timerange() arg 3 must not be timedelta(0)'
        with pytest.raises(ValueError, message=msg):
            jt.timerange(datetime(2017, 1, 1), datetime(2017, 2, 2), timedelta())

    def test_init_raise_type_error(self):
        msg = 'timerange() arg {} must be date or datetime object'
        with pytest.raises(TypeError, message=msg.format(1)):
            jt.timerange(100, datetime(2017, 2, 3))
        with pytest.raises(TypeError, message=msg.format(2)):
            jt.timerange(date(2017, 2, 3), 4)
        with pytest.raises(TypeError, message=msg.format(3)):
            jt.timerange(date(2017, 2, 3), date(2017, 4, 5), 24 * 60 * 60)

    @pytest.mark.parametrize('start, stop, step, results', [
        (date(1970, 1, 1), date(1970, 2, 1), 15 * jt.DAY,
         [date(1970, 1, 1), date(1970, 1, 16), date(1970, 1, 31)]),

        (date(1, 1, 1), date(2, 2, 2), 365 * jt.DAY,
         [date(1, 1, 1), date(2, 1, 1)]),

        (date(2, 2, 2), date(1, 1, 1), -365 * jt.DAY,
         [date(2, 2, 2), date(1, 2, 2)]),

        (date(1, 1, 1), date(1, 1, 1), jt.DAY, []),
        (date(1, 1, 1), date(1, 1, 1), -jt.DAY, []),
    ])
    def test_iter_date(self, start, stop, step, results):
        assert list(jt.timerange(start, stop, step)) == results

    @pytest.mark.parametrize('start, stop, step, results', [
        (datetime(1970, 1, 1), datetime(1970, 1, 1, 23), 10 * jt.HOUR,
         [datetime(1970, 1, 1), datetime(1970, 1, 1, 10),
          datetime(1970, 1, 1, 20)]),

        (datetime(1, 1, 1, 1), datetime(2, 2, 2, 2), 365 * jt.DAY,
         [datetime(1, 1, 1, 1), datetime(2, 1, 1, 1)]),

        (datetime(2, 2, 2, 2), datetime(1, 1, 1, 1), -365 * jt.DAY,
         [datetime(2, 2, 2, 2), datetime(1, 2, 2, 2)]),

        (datetime(2, 2, 2, 2), datetime(2, 2, 2, 2), jt.MICROSECOND, []),
        (datetime(2, 2, 2, 2), datetime(2, 2, 2, 2), -jt.MICROSECOND, [])
    ])
    def test_iter_datetime(self, start, stop, step, results):
        assert list(jt.timerange(start, stop, step)) == results

    def test_equal(self):
        assert jt.timerange(
            date(1, 1, 1), date(1, 1, 1)
        ) == jt.timerange(
            date(1, 1, 1), date(1, 1, 1)
        )

    def test_start_not_equal(self):
        assert jt.timerange(
            date(1, 1, 1), date(1, 1, 1)
        ) != jt.timerange(
            date(1, 1, 2), date(1, 1, 1)
        )

    def test_stop_not_equal(self):
        assert jt.timerange(
            date(1, 1, 2), date(1, 1, 1)
        ) != jt.timerange(
            date(1, 1, 2), date(1, 1, 2)
        )

    def test_step_not_equal(self):
        assert jt.timerange(
            date(1, 1, 2), date(1, 1, 2), jt.DAY
        ) != jt.timerange(
            date(1, 1, 2), date(1, 1, 2), jt.MINUTE
        )

    def test_type_not_equal(self):
        assert jt.timerange(
            datetime(1, 1, 1), datetime(1, 1, 1)
        ) != timedelta(1)

    def test_hash(self):
        assert hash(jt.timerange(
            date(1, 1, 1), date(1, 1, 1)
        )) == hash(jt.timerange(
            date(1, 1, 1), date(1, 1, 1)
        ))


@pytest.mark.parametrize('arg, res', [
    (datetime(2017, 11, 24, 1), datetime(2017, 11, 1, 1)),
    (datetime(1970, 1, 1, 1, 1, 1), datetime(1970, 1, 1, 1, 1, 1)),
    (date(2222, 2, 28), date(2222, 2, 1)),
])
def test_this_month_first_day(arg, res):
    assert jt.this_month_first_day(arg) == res


@pytest.mark.parametrize('arg, res', [
    (datetime(2017, 11, 24, 1), datetime(2017, 11, 30, 1)),
    (datetime(1970, 1, 1, 1, 1, 1), datetime(1970, 1, 31, 1, 1, 1)),
    (date(2222, 2, 28), date(2222, 2, 28)),
    (date(2000, 2, 23), date(2000, 2, 29)),
    (datetime(2017, 8, 3), datetime(2017, 8, 31)),
])
def test_this_month_last_day(arg, res):
    assert jt.this_month_last_day(arg) == res


@pytest.mark.parametrize('arg, res', [
    (datetime(2017, 12, 31), datetime(2017, 11, 1)),
    (datetime(2016, 1, 29, second=23), datetime(2015, 12, 1, second=23)),
    (date(2000, 1, 1), date(1999, 12, 1)),
])
def test_prev_month_first_day(arg, res):
    assert jt.prev_month_first_day(arg) == res


@pytest.mark.parametrize('arg, res', [
    (datetime(2017, 3, 31), datetime(2017, 2, 28)),
    (datetime(2016, 3, 31), datetime(2016, 2, 29)),
    (datetime(2017, 12, 31), datetime(2017, 11, 30)),
    (datetime(2016, 1, 29, second=23), datetime(2015, 12, 31, second=23)),
    (date(2000, 1, 1), date(1999, 12, 31)),
])
def test_prev_month_last_day(arg, res):
    assert jt.prev_month_last_day(arg) == res


@pytest.mark.parametrize('arg, res', [
    (datetime(2017, 1, 31), datetime(2017, 2, 1)),
    (datetime(2016, 1, 15), datetime(2016, 2, 1)),
    (datetime(2017, 12, 31), datetime(2018, 1, 1)),
    (datetime(2016, 7, 29, hour=23), datetime(2016, 8, 1, hour=23)),
    (date(2000, 1, 1), date(2000, 2, 1)),
])
def test_next_month_first_day(arg, res):
    assert jt.next_month_first_day(arg) == res


@pytest.mark.parametrize('arg, res', [
    (datetime(2017, 1, 31), datetime(2017, 2, 28)),
    (datetime(1899, 12, 15), datetime(1900, 1, 31)),
    (datetime(2017, 10, 31), datetime(2017, 11, 30)),
    (datetime(2016, 5, 9, microsecond=1), datetime(2016, 6, 30, microsecond=1)),
    (date(2000, 1, 1), date(2000, 2, 29)),
])
def test_next_month_last_day(arg, res):
    assert jt.next_month_last_day(arg) == res
