import pytest
from sblex.saldo_ws.config import MatomoSettings


class TestMatomoSettings:
    def test_url_without_idsite_raises_value_error(self, snapshot) -> None:
        with pytest.raises(ValueError) as exc:
            MatomoSettings(matomo_url="http://example.com")
        assert str(exc) == snapshot
