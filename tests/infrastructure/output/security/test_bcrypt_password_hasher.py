from infrastructure.output.security.bcrypt_password_hasher import BcryptPasswordHasher


def test_hash_is_not_plaintext_and_can_be_verified():
    hasher = BcryptPasswordHasher(rounds=4)

    password_hash = hasher.hash("a-secure-password")

    assert password_hash != "a-secure-password"
    assert password_hash.startswith("$2")
    assert hasher.verify("a-secure-password", password_hash)
    assert not hasher.verify("wrong-password", password_hash)


def test_verify_returns_false_for_invalid_hash():
    hasher = BcryptPasswordHasher(rounds=4)

    assert not hasher.verify("a-secure-password", "not-a-valid-bcrypt-hash")


def test_hash_supports_passwords_longer_than_bcrypt_byte_limit():
    hasher = BcryptPasswordHasher(rounds=4)
    password = "secure-phrase-" * 20

    password_hash = hasher.hash(password)

    assert hasher.verify(password, password_hash)
