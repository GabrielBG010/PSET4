from contextlib import contextmanager
import tempfile
import os


@contextmanager
def atomic_write(file, mode="w", as_file=True, **kwargs):
    """Write a file atomically

    :param file: str or :class:`os.PathLike` target to write

    :param bool as_file:  if True, the yielded object is a :class:File.
        (eg, what you get with `open(...)`).  Otherwise, it will be the
        temporary file path string

    :param kwargs: anything else needed to open the file

    :raises: FileExistsError if target exists

    Example::

        with atomic_write("hello.txt") as f:
            f.write("world!")

    """
    # checking of "file" type
    temporary_file = None
    try:
        if as_file:
            # it is not a class file
            file_directory = os.path.dirname(file)
            temporary_file = tempfile\
                .NamedTemporaryFile(delete=False,
                                    dir=file_directory, mode=mode)

        else:
            temporary_file = file

        if os.path.isfile(file):
            raise FileExistsError()

        # yielding of the file
        yield temporary_file

        # closing of the file
        temporary_file.close()

        # renaming of the file
        os.rename(temporary_file.name, file)

    except FileExistsError as err:
        raise err
    except IOError as err:
        if os.path.exists(temporary_file.name):
            temporary_file.close()
            os.remove(temporary_file.name)
        raise err
