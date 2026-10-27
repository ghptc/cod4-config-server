"""Mode policy contract; native voting behavior is tested in the engine suite."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]


class ZombiesVoting(unittest.TestCase):
    def test_native_map_votes_only(self):
        cfg = (ROOT / 'modes/zombies/server.cfg').read_text()
        pairs = re.findall(r'^set (\w+) "([^"\n]*)"$', cfg, re.M)
        values = dict(pairs)
        self.assertEqual(len(pairs), len(values), 'ambiguous repeated mode setting')
        expected = {'g_allowVote': '1', 'g_oldVoting': '1',
                    'g_voteAllowMap': '1', 'g_voteAllowMaprotate': '1',
                    'g_voteAllowRestart': '0', 'g_voteAllowGametype': '0',
                    'g_voteAllowKick': '0', 'g_voteCooldown': '5',
                    'g_voteAbstainWeight': '1', 'sv_pure': '1', 'bot_enable': '0'}
        for name, value in expected.items():
            with self.subTest(name=name):
                self.assertEqual(values[name], value)
        maps = re.findall(r'\bmap (mp_\w+)', values['sv_mapRotation'])
        self.assertIn('mp_crash', maps)
        self.assertNotIn('mp_killhouse', maps, 'requires supervised qualification')
        self.assertEqual(len(maps), 15)
