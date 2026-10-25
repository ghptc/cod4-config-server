# Provenance and publication review

Review date: 2026-10-25.

## Initial state

Local Git was already initialized on unborn `master`, with no commits, tracked
files or remotes. Existing untracked files were not presumed publishable.
Authenticated GitHub lookup could not resolve `ghptc/cod4-promod-server`.
Remote creation is required if the name is indeed absent; access limitations
can also cause this response. No remote was created or overwritten.

## Included work

New English documentation, a sanitized declarative configuration example,
asset fingerprints, an original read-only Python verifier and an explicit Git
allowlist. Existing configuration values supply operating settings only;
credentials, personal naming and temporary developer logging are omitted.
No blanket open-source license is assigned to third-party or unverified work.
Owner license selection for original repository material remains pending.

## Excluded material

- `game/mods/pml220/mod.ff`, `pml220.iwd`: installed Promod/game-derived assets;
  identified as LIVE V2.20 EU by existing engine evidence, not traced to a
  verified release archive. The IWD contains images, sounds and weapon data.
- `z_c_r.iwd`: contains `promod_ruleset/custom_public.gsc`; upstream/custom
  delta and authorship unverified. It is not established as the 333 FPS patch.
- Localized header IWDs and all eight administrative header data files:
  generated/game-derived inputs. Preserved privately and fingerprinted.
- Existing `tools/build_localized_headers.py` and `tools/iwd_checksum.py`:
  authorship unverified, integrity work outside this repository's scope.
  The former handles only seven localized inputs; it cannot reproduce the
  eighth `jcod4x_00.dat`. The latter is not verified as engine checksum parity.
- `.env`, runtime configuration, game home, logs, status files, backups,
  downloads, compose variants and infrastructure directories: private runtime,
  generated output or orchestration owned elsewhere. None is published.

## Licensing findings

Reviewed upstream `cod4mw/promod` LICENSE.md at exact revision
`d22de10be2625674f252be29448530220db48228` via GitHub API:
https://github.com/cod4mw/promod/blob/d22de10be2625674f252be29448530220db48228/LICENSE.md

PModEPL 1.0 grants use, derivative works, hosting and redistribution for covered
mod assets. Conditions include dated modifications, retained notices and terms,
readily available modifiable sources, and licensing under PModEPL. It excludes
original-game/tool assets from its covered mod-asset definition. Activision
map-tools terms also apply; upstream references a separate complete EULA.
That complete EULA was not available in the inspected installation. This public
source license does not establish provenance or permission for every installed
binary, embedded game asset or third-party customization.

No FF, IWD, GSC, extracted source or third-party data is staged. Publication of
those files remains blocked until exact provenance, complete applicable terms,
notices and source obligations are verified. The 333 FPS modification remains
unidentified; preserve its existing installation pending source recovery.

## Validation limits

SHA-256 identity validation covers three installed Promod inputs and all eight
headers using `assets.json`. Full fastfile compilation, authorized acquisition,
333 FPS behavior and runtime gameplay reproduction remain unverified. There
were no service changes, EC2 access, deployment or asset deletion/movement.
