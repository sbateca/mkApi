from infrastructure.output.security.refresh_token_adapter import RefreshTokenAdapter


def test_generate_returns_unique_high_entropy_tokens():
    adapter = RefreshTokenAdapter()

    first = adapter.generate()
    second = adapter.generate()

    assert first != second
    assert len(first) >= 64


def test_digest_is_deterministic_and_does_not_store_plaintext():
    adapter = RefreshTokenAdapter()

    digest = adapter.digest("refresh-token")

    assert digest == adapter.digest("refresh-token")
    assert digest != "refresh-token"
    assert len(digest) == 64
