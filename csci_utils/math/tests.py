from unittest import TestCase
import numpy as np
from csci_utils.math import cosine_similarity


class CosineSimTests(TestCase):
    def test_cosine_sim(self):
        """test if cosine similarity calculates edge cases correctily"""

        a = np.array([1,1])

        # check identical vector
        self.assertAlmostEqual(cosine_similarity(a,np.array([1,1])),1.0)

        # check vector in same direction
        self.assertAlmostEqual(cosine_similarity(a, np.array([5, 5])), 1.0)

        # check orthogonal vector
        self.assertAlmostEqual(cosine_similarity(a, np.array([1, -1])), 0.0)

        # check antiparellel vector
        self.assertAlmostEqual(cosine_similarity(a, np.array([-1, -1])), -1.0)





