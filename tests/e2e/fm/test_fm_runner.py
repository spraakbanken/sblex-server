from pathlib import Path

import pytest
from sblex.fm import FMrunner


@pytest.fixture(name="fm_runner")
def fixture_fm_runner() -> FMrunner:
    return FMrunner(Path("./bin/saldo"))


def test_fm_runner(fm_runner):
    assert fm_runner.inflection("vb_vs_dväljas", "dväljas") == [
        {
            "word": "dväljes",
            "head": "dväljas",
            "pos": "vb",
            "param": "pres ind s-form",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dväljs",
            "head": "dväljas",
            "pos": "vb",
            "param": "pres ind s-form",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dvaldes",
            "head": "dväljas",
            "pos": "vb",
            "param": "pret ind s-form",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dväljdes",
            "head": "dväljas",
            "pos": "vb",
            "param": "pret ind s-form",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dväljes",
            "head": "dväljas",
            "pos": "vb",
            "param": "imper",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dväljs",
            "head": "dväljas",
            "pos": "vb",
            "param": "imper",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dväljas",
            "head": "dväljas",
            "pos": "vb",
            "param": "inf s-form",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dvalts",
            "head": "dväljas",
            "pos": "vb",
            "param": "sup s-form",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
        {
            "word": "dvälts",
            "head": "dväljas",
            "pos": "vb",
            "param": "sup s-form",
            "inhs": [],
            "id": "dväljes_vb",
            "p": "vb_vs_dväljas",
            "attr": "0",
        },
    ]
