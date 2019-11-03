from atomicwrites import atomic_write as _backend_writer, AtomicWriter
from pathlib import Path
from contextlib import contextmanager
import os
import io
import tempfile


class SuffixWriter(AtomicWriter):
    """Modified AtomicWriter class that saves temporary files with the same suffix as the target file

    Usage::
        with AtomicWriter(path).open() as f:
            f.write(...)
    :param path: The destination filepath. May or may not exist.
    :param mode: The filemode for the temporary file. This defaults to `wb` in
        Python 2 and `w` in Python 3.
    :param overwrite: If set to false, an error is raised if ``path`` exists.
        Errors are only raised after the file has been written to.  Either way,
        the operation is atomic.
    :param **kwargs dict: parameters passed to io.open()
    """

    def get_fileobject(self, dir=None, **kwargs):
        """Return the temporary file to use with the same suffix as the target."""

        if dir is None:
            dir = os.path.normpath(os.path.dirname(self._path))

        # get suffix (allows for more than one, e.g. .tar.gz) and pass it to tempfile.mkstemp
        suffix = "".join(Path(self._path).suffixes)

        descriptor, name = tempfile.mkstemp(
            suffix=suffix, prefix=tempfile.template, dir=dir
        )
        # io.open() will take either the descriptor or the name, but we need
        # the name later for commit()/replace_atomic() and couldn't find a way
        # to get the filename from the descriptor.
        os.close(descriptor)
        kwargs["mode"] = self._mode
        kwargs["file"] = name

        return io.open(**kwargs)


@contextmanager
def atomic_write(file, mode="w", as_file=True, overwrite=False, **kwargs):
    """Function that performs atomic writes using the atomic_write function from atomicwrites as a backend

    :param file str or Path-like: target file name
    :param mode str: write mode that gets passed down to io.open()
    :param as_file bool: flag to either yield file handle if True or file name of temporary file if False
    :param overwrite bool: flag that tells to overwrite existing target file if True or raise FileExistsError if False
    :param **kwargs dict: kwargs that ultimately get passed down to io.open()
    """

    # SuffixWriter/AtomicWriter handles these as kwargs
    kwargs["mode"] = mode
    kwargs["overwrite"] = overwrite

    # use original atomic write as backend, but pass in SuffixWriter as writer class
    with _backend_writer(file, writer_cls=SuffixWriter, **kwargs) as f:
        # depending on as_file return file handle or file name
        if as_file:
            yield f
        else:
            yield f.name
