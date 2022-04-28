import os
import unittest
import definitions as defs


class TestPupil(unittest.TestCase):
    def setUp(self):
        self.ref_image_path = os.path.join(defs.DATA_DIR, "images/ref_image_new.jpg")

    def test_something(self):
        self.assertEqual(True, True)


if __name__ == "__main__":
    unittest.main()
