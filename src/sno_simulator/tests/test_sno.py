import pytest
from sno_simulator.sno import SnøLag, Sno, Is


@pytest.fixture
def sno():
    return Sno(0.05)


@pytest.fixture
def is_():
    return Is(0.08)


@pytest.fixture
def lag():
    return SnøLag(0.05, 0.08)


def test_snofall(sno):
    sno.snøfall(10)
    assert sno.dybde == 10


def test_snøsmelting_1(sno):
    sno.snøfall(10)
    smeltet = sno.smelting(1)
    assert smeltet == 0
    assert sno.dybde == 9.5


def test_snøsmelting_2(sno):
    sno.snøfall(10)
    smeltet = sno.smelting(13)
    assert smeltet == 6.5
    assert sno.dybde == 3.5


def test_snøsmelting_alt(sno):
    sno.snøfall(10)
    smeltet = sno.smelting(30)
    assert smeltet == 10


def test_is_dannelse(is_):
    is_.dannelse(10)
    assert is_.dybde == 10


def test_is_smelting(is_):
    is_.dannelse(10)
    smeltet = is_.smelting(1)
    assert smeltet == 0.8
    assert is_.dybde == 9.2


def test_lag_snøfall(lag):
    lag.snøfall(10)
    assert lag.topp_lag.dybde == 10


def test_lag_smelting(lag):
    lag.snøfall(10)
    lag.smelting(1)
    assert lag.topp_lag.dybde == 9.5


def test_lag_smelting_alt_et_lag(lag):
    lag.snøfall(10)
    vann = lag.smelting(20)
    assert vann == 10
    assert len(lag.lag) == 0


def test_flere_lag_snø_is(lag):
    lag.snøfall(10)
    lag.minus()
    assert len(lag.lag) == 1


def test_flere_lag_snø_smelting_is(lag):
    lag.snøfall(10)
    lag.smelting(1)
    lag.minus()
    assert len(lag.lag) == 2
    assert lag.topp_lag.dybde == 0.5


def test_flere_lag_snø_smelting_is_sno(lag):
    lag.snøfall(10)
    vann_i_systemet = lag.smelting(1)
    assert vann_i_systemet == 0
    lag.minus()
    lag.snøfall(10)
    assert len(lag.lag) == 3
    assert lag.topp_lag.dybde == 10


def test_flere_lag_snø_is_smelting(lag):
    lag.snøfall(10)
    lag.smelting(1)
    lag.minus()
    vann_i_systemet = lag.smelting(1)
    assert vann_i_systemet == 0
    assert len(lag.lag) == 2
    assert lag.topp_lag.dybde == 0.46


def test_ingen_snø_minus(lag):
    lag.lag.pop()
    lag.snøfall(0)
    lag.minus()
    assert lag.dybde == 0


def test_ingen_snø_smelting(lag):
    lag.lag.pop()
    vann_i_systemet = lag.smelting(1)
    assert vann_i_systemet == 0
    assert lag.dybde == 0
