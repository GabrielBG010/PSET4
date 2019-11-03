from unittest import TestCase
from os import environ
from contextlib import contextmanager

from csci_utils.hashing import hash_str, get_user_id, get_csci_salt


class FakeFileFailure(IOError):
    pass


@contextmanager
def FakeEnviron():
    """defines a context manager that temporarily changes the environment variable CSCI_SALT"""

    fake_salt = "FAKE_SALT".encode()
    real_salt = environ["CSCI_SALT"]  # store the real salt in a variable
    environ[
        "CSCI_SALT"
    ] = fake_salt.hex()  # overwrite the environment variable with fake value
    try:
        yield  # context block here
    finally:
        environ[
            "CSCI_SALT"
        ] = real_salt  # make sure that original salt is written back to environment


class HashTests(TestCase):
    def test_basic(self):
        self.assertEqual(hash_str("world!", salt="hello, ").hex()[:6], "68e656")

    def test_input_hash(self):
        """Check various input types for hash_str function"""

        # test that salt is accepted as bytes input
        self.assertEqual(
            hash_str("world!", salt="hello, ".encode()).hex()[:6], "68e656"
        )
        # test that wrong type for first argument raises an Error
        self.assertRaises(TypeError, hash_str, 1, salt="test")
        # test that wrong type for salt raises an Error
        self.assertRaises(TypeError, hash_str, "test", salt=1)

    def test_get_csci(self):
        """Test for hashing User ID while retrieving salt from environment"""

        with FakeEnviron():
            self.assertEqual(get_csci_salt(), "FAKE_SALT".encode())

    def test_user_id(self):
        """Test for hashing User ID while retrieving salt from environment"""

        with FakeEnviron():
            self.assertEqual(
                get_user_id("fake-name"), "c5b4d72d"
            )  # this control value was obtained by sha256 hashing 'fake-name' with the fake salt
