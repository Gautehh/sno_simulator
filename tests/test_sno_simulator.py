from io import TextIOWrapper
from typing import Iterator
import pytest
import os
from src.sno_simulator.simulator import snø_simulator
from src.sno_simulator.sno import SnøLag



@pytest.fixture
def get_current_dir():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def sno_test_file(get_current_dir) -> Iterator[TextIOWrapper]:
    with open(f"{get_current_dir}/assets/sno_geilo_sample.csv") as f:
        yield f


@pytest.fixture
def sno_geilo_file(get_current_dir) -> Iterator[TextIOWrapper]:
    with open(f"{get_current_dir}/assets/sno_geilo.csv") as f:
        yield f


def test_sno_simulator_ett_lag(sno_test_file: Iterator[TextIOWrapper]):
    snø_lag = SnøLag(0.05, 0.08)
    tid, vann_i_systemet, snø_dybde = snø_simulator(sno_test_file, snø_lag)
    assert tid == [
        "2022-10-01 01:00:00",
        "2022-10-01 02:00:00",
        "2022-10-01 03:00:00",
        "2022-10-01 04:00:00",
        "2022-10-01 05:00:00",
    ]
    assert vann_i_systemet == [0, 0, 0, 0, 0]
    assert snø_dybde == [2.0, 3.0, 2.55, 6.0, 5.82]
