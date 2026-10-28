from pathlib import Path
import re
import unittest
ROOT = Path(__file__).resolve().parents[1]


class MilitaryNames(unittest.TestCase):
    def test_configured_pool_contains_both_groups_and_fits_native_limits(self):
        names = (ROOT / 'modes/promod/botnames.txt').read_text().splitlines()
        self.assertEqual(len(names), 15)
        self.assertEqual(len(set(n.lower() for n in names)), 15)
        self.assertTrue({'Capt. Price', 'Soap MacTavish', 'Capt. MacMillan',
                         'Sgt. Miller', 'Capt. Mitchell'}.issubset(names))
        self.assertTrue(all(len(n) <= 31 and re.fullmatch('[A-Za-z0-9. -]+', n) for n in names))
        cfg = (ROOT / 'modes/promod/server.cfg').read_text()
        self.assertIn('set bot_use_names "1"', cfg)
        self.assertIn('set bot_sd_objectives "1"', cfg)
        self.assertNotIn('bot_use_names', (ROOT / 'modes/zombies/server.cfg').read_text())
