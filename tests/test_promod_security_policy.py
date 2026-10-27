"""Canonical rules run after private CFGs and must not silently enable Auto-Fill."""
from pathlib import Path
import shlex
import unittest

ROOT = Path(__file__).resolve().parents[1]


def apply_catalog_cfg(settings, path):
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith('//'):
            continue
        words = shlex.split(line)
        # These catalogs are data-only set commands; reject an unreviewed command
        # rather than silently ignoring a future indirect policy override.
        if len(words) != 3 or words[0].lower() != 'set':
            raise AssertionError('Unreviewed catalog command in ' + str(path))
        settings[words[1].lower()] = words[2]


class PromodSecurityPolicy(unittest.TestCase):
    def resolve(self, private_choice=None):
        # Native SV_BotManagerInit at the reviewed release revision defaults off.
        settings = {'bot_enable': '0'}
        apply_catalog_cfg(settings, ROOT / 'shared/server.cfg')
        if private_choice is not None:
            settings['bot_enable'] = private_choice
        apply_catalog_cfg(settings, ROOT / 'modes/promod/server.cfg')
        return settings

    def test_security_release_does_not_enable_default_autofill(self):
        self.assertEqual(self.resolve()['bot_enable'], '0')

    def test_private_autofill_choice_survives_final_mode_rules(self):
        for choice in ('0', '1'):
            with self.subTest(private_choice=choice):
                settings = self.resolve(choice)
                self.assertEqual(settings['bot_enable'], choice)
                self.assertEqual(settings['bot_fill_limit'], '12')
                self.assertEqual(settings['sv_pure'], '1')
                self.assertEqual(settings['g_gametype'], 'sd')


if __name__ == '__main__':
    unittest.main()
