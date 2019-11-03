import os
from tempfile import TemporaryDirectory
from unittest import TestCase

from csci_utils.io import atomic_write


class FakeFileFailure(IOError):
    pass


class AtomicWriteTests(TestCase):
    def test_atomic_write(self):
        """Ensure file exists after being written successfully"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w") as f:
                assert not os.path.exists(fp)
                tmpfile = f.name
                f.write("asdf")

            assert not os.path.exists(tmpfile)
            assert os.path.exists(fp)

            with open(fp) as f:
                self.assertEqual(f.read(), "asdf")

    def fake_file_fail(self, fp):
        """Start an atomic write of  and make it fail

        :param str fp: filename to write to

        :return str tmpfilename: that was written and hopefully deleted"""

        with self.assertRaises(FakeFileFailure):
            with atomic_write(fp, "w") as f:
                tmpfile = f.name
                assert os.path.exists(tmpfile)
                raise FakeFileFailure()
        return tmpfile

    def test_atomic_failure(self):
        """Ensure that file does not exist after failure during write"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            # perform an atomic write that is guaranteed to have failed
            tmpfile = self.fake_file_fail(fp)

            assert not os.path.exists(tmpfile)
            assert not os.path.exists(fp)

    def test_file_exists(self):
        """Ensure an error is raised when a file exists"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            def one_write():
                with atomic_write(fp, "w") as f:
                    f.write("asdf")

            one_write()
            self.assertRaises(FileExistsError, one_write)

    def test_extension(self):
        """test if the filename is returned when the as_file flag is False and the filetype is correct"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            with atomic_write(fp, "w", as_file=False) as f:
                self.assertEqual(os.path.splitext(f)[1], ".txt")

    def test_repeat(self):
        """test if after 1 failed write the 2nd write does not reopen the same tmp file"""

        with TemporaryDirectory() as tmp:
            fp = os.path.join(tmp, "asdf.txt")

            # perform an atomic write that is guaranteed to have failed
            tmpfile1 = self.fake_file_fail(fp)

            # then in the same dir  generate another atomic write and check if the filename is the same
            with atomic_write(fp, "w") as f:
                tmpfile2 = f.name

            self.assertNotEqual(tmpfile1, tmpfile2)
