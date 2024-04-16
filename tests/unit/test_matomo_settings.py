import json

import pytest
from pydantic import ValidationError
from sblex.saldo_ws.config import MatomoSettings


class TestMatomoSettings:
    def test_url_without_idsite_raises_value_error(self, snapshot) -> None:
        with pytest.raises(ValidationError) as exc:
            MatomoSettings(matomo_url="http://example.com")
        assert json.loads(exc.value.json())[0]["msg"] == snapshot
