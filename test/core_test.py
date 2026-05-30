import unittest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

class TestCore(unittest.TestCase):    
    def test_import_core(self):
        try:
            from core.core import CoreWindow
            self.assertIsNotNone(CoreWindow)
        except ImportError as e:
            self.fail(f"Import error: {e}")

if __name__ == '__main__':
    unittest.main()