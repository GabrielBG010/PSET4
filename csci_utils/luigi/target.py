from luigi.local_target import LocalTarget, atomic_file
from contextlib import contextmanager
import random


class suffix_preserving_atomic_file(atomic_file):
    def generate_tmp_path(self, path):

        # Get the extension to the path.
        # First find the index of the first .
        idx = path.find('.')

        # Slice the path on . and store the extension
        ext = path[idx:]

        # Tac the ext onto the returned path.
        return path + '-luigi-tmp-%09d' % random.randrange(0, 1e10) + ext


class BaseAtomicProviderLocalTarget(LocalTarget):
    # Allow some composability of atomic handling
    atomic_provider = atomic_file

    def open(self, mode='r'):
        # leverage super() as well as modifying any code in LocalTarget
        # to use self.atomic_provider rather than atomic_file

        rwmode = mode.replace('b', '').replace('t', '')
        # if mode is 'r' then call super() which will use the parents method to handel this case.
        if mode == 'r':
            super(open, self).open(mode='r')

        # if the mode is 'w' then override the parent method by replacing atomic_file with self.atomic_provider.
        if rwmode == 'w':
            self.makedirs()
            return self.format.pipe_writer(self.atomic_provider(self.path))
        else:
            raise Exception("mode must be 'r' or 'w' (got: %s)" % mode)

    @contextmanager
    def temporary_path(self):
        # NB: unclear why LocalTarget doesn't use atomic_file in its implementation
        self.makedirs()
        with self.atomic_provider(self.path) as af:
            yield af.tmp_path


class SuffixPreservingLocalTarget(BaseAtomicProviderLocalTarget):
    atomic_provider = suffix_preserving_atomic_file
