# CoD4 configuration catalog

Canonical repository: https://github.com/ghptc/cod4-config-server

Only `promod` (Promod LIVE 2.20) is implemented. Before the Dawn Zombies and
Hardcore are future modes, pending real configuration, authorized assets and
compatibility tests. There are no placeholder modes or new bot settings here.

## Ownership

- `shared/server.cfg`: catalog defaults for purity, voice and download policy.
  These are operator policies, not claims about every mod's capabilities.
- `modes/<id>/mode.cfg`: startup selection metadata only (`fs_game`).
- `modes/<id>/server.cfg`: mode identity, capacity, game type, rules and rotation.
  Promod keeps 12 slots, Search and Destroy, `match_mr12_pb`, and Crash, Strike,
  Crossfire, Backlot in that order. No logging or network settings are invented.

A new mode adds its own directory without editing existing modes. Shared settings
are defaults; a mode may explicitly override a shared key when compatibility
requires it. Document each overlap with `// Override shared: <setting>` on its
own line in the mode file and review it. There are currently no overlaps.
Private runtime settings load last.

The engine, bots and compatibility fixes belong to `cod4x-server`. Builds,
asset verification, Compose, SSH, deployment and rollback belong to
`ec2-workspace`. This repository contains only public configuration and this
contract; no application code, runtime assets or deployment scripts.

## Discovery and validation contract

The consumer must apply these checks before preparing or changing a runtime:

1. Read a clean detached checkout at an exact reviewed configuration commit SHA.
   Discover immediate directories under `modes/`, sorted in byte order
   (`LC_ALL=C`). An identifier is its case-sensitive directory name matching
   `[a-z][a-z0-9-]*`. IDs are unique; reject symlinks and invalid names. Select
   exactly the requested ID, with no alias, default or fallback. A malformed
   directory is an error, not an available mode to silently skip.
2. Require nonempty regular, nonsymlink `shared/server.cfg`, and `mode.cfg` and
   `server.cfg` in each mode. Read only these contract files; never scan the
   historical local directories for configuration. Discovery uses the complete
   catalog; asset qualification is required only for the selected mode.
3. CFGs use a deliberately small subset of native syntax: blank lines, full-line
   `//` comments, and one `set name "value"` per line. Names match
   `[A-Za-z_][A-Za-z0-9_]*`; values contain no quotes, backslashes, semicolons or
   control characters. No shell evaluation, `exec`, command chaining or duplicate
   keys within a file. Review variables against the selected engine/mod; syntax
   validation alone cannot prove that a mod implements a variable.
4. `mode.cfg` contains exactly one setting: `set fs_game "mods/<directory>"`,
   where `<directory>` matches `[A-Za-z0-9_-]+`, or `set fs_game ""` for base-game
   modes. No traversal or absolute paths. `fs_game` and other filesystem startup
   settings must not appear in shared/gameplay CFGs. Do not execute `mode.cfg`
   after startup: parse its literal value into a separate `+set fs_game` argv pair.
5. The effective shared-plus-mode settings must include nonempty `sv_hostname`,
   positive integer `sv_maxclients`, `g_gametype`, and `sv_mapRotation`. Rotation
   uses one or more `gametype <name> map <name>` groups (names match
   `[A-Za-z0-9_]+`); its first game type must match `g_gametype`. Its first map is
   the startup map, so no separate startup-map metadata is required. Verify slot
   limits, game types and all maps against the authorized selected assets.
6. Reject credentials in public files and undocumented shared/mode overlaps.
   Require authorized, verified runtime assets for the selected `fs_game`; for a
   mod this includes its `mod.ff` and required IWDs/maps. Missing configuration,
   unsupported variables or unqualified assets fail before runtime mutation.
   Bot support, Promod patches and build steps are never assumed for other mods.

This is the contract for the separate consumer implementation. The current
`ec2-workspace` still reads `config/promod.cfg` and does not yet implement these
checks or this layout. Coordinate that PR before adopting this catalog commit.
Older configuration commits remain usable by the existing consumer.

## Packaging and loading order

Package immutable copies of `shared/server.cfg` and the selected
`modes/<id>/server.cfg` as `canonical-shared.cfg` and `canonical-mode.cfg` in the
selected game search path (`mods/<directory>/`, or `main/` for empty `fs_game`).
Retain `mode.cfg` as artifact provenance; never mount the live Git checkout into
running containers. Record mode ID, configuration SHA, the three CFG hashes,
engine revision, authorized asset identities and immutable image identity.

1. At process startup, pass exactly one `+set fs_game <literal-value>` before
   configuration execution. Base game requires an explicit empty argv element.
2. Execute `+exec canonical-shared.cfg`, then `+exec canonical-mode.cfg`.
3. Load the existing private runtime overrides in their existing relative order.
   Preserve their files and credentials. Reject conflicting filesystem selection
   arguments before launch; do not let inherited settings silently change modes.
4. Start the first map from the selected rotation after configuration loading.
   An existing explicit private startup-map override retains precedence only if
   validated as compatible with the selected mode.

Switching modes requires an explicit container recreation using qualified assets
and this startup sequence, with health checks and rollback. A matching `fs_game`
alone is insufficient to identify a mode: base-game modes can share that value.
Removing a catalog directory does not stop, modify or invalidate an already
packaged/approved deployment. Production promotes the approved artifact without
resolving the latest catalog; selecting a removed mode for a new build fails.

## Required separate ec2-workspace PR

Keep the existing interfaces:

```sh
./scripts/deploy-homolog.sh promod
./scripts/deploy-production.sh promod
./scripts/game-mode.sh homolog promod
```

- `scripts/common.sh`, `resolve_master`/`checkout_master`: replace the old
  `ghptc/cod4-promod-server` URL with `ghptc/cod4-config-server`; accept a pinned
  config SHA, discover/validate the catalog once, and resolve the requested ID.
  Replace the old `config/promod.cfg` existence check with the contract above.
- `deploy` and `build_promod`: replace the literal Promod-only argument gate and
  packaging path with the selected-mode contract. Package shared and mode CFGs;
  resolve authorized assets by selected `fs_game`, including empty/base-game.
  Isolate existing Promod Bot Warfare/FPS/integrity preparation behind verified
  Promod asset requirements; never apply it to Zombies or Hardcore. Generic
  packaging must accept qualified assets without adding a mode-name switch list.
- `image_config`, `runtime_mode`, `verify_homolog`, `deploy_image`: use the
  selected startup value, ordered CFG execs and validated first map. Record and
  verify mode ID/config hashes with image identity, rather than identifying a
  mode by `fs_game` or Promod-specific labels alone. Preserve private overrides,
  mounts, approvals, health checks and rollback. Retain compatibility with
  existing approved artifacts; do not reinterpret their contents as this layout.
- `scripts/game-mode.sh`: replace the hardcoded gate, `mods/pml220` substitution
  and same-`fs_game` early return. Explicitly select a qualified mode artifact,
  recreate with its full startup contract, and roll back on failure. No in-process
  `fs_game` change. Production switching must retain homolog approval controls.
- `.state` prepared/approved records: bind mode ID, config SHA/hashes and assets
  to the immutable artifact. Production must compare the requested ID with that
  approval, without fetching the latest catalog or rebuilding.
- `tests/operations.sh` and `README.md`: update fixtures and old repository link;
  test discovery, invalid/incomplete modes, overrides, exact SHA provenance,
  empty `fs_game`, mode isolation, explicit switching, removal after approval,
  and production approval/rollback. Future-mode fixtures are contract tests,
  not claims of working Zombies or Hardcore gameplay.

No sibling repository or deployed container was changed for this refactor.

## Historical local files

All private files remain in place under explicit ignore rules:

| Paths | Classification / disposition |
| --- | --- |
| `config/server.cfg`, `config/server.example.cfg` | Redundant historical configuration, retained locally; archive candidates after runtime migration. |
| `game/mods/` | Required private assets; provenance/redistribution rights not established by this repository. |
| `game/home/`, `artifacts/` | Generated runtime state, logs and game-derived integrity artifacts; retain privately. |
| `tools/`, `assets.json` | Historical integrity/build tooling and fingerprints; retain for ownership review outside this catalog. |
| `compose*.yaml` | Historical orchestration; retain for workspace review. Main/backup duplicate one another; the pure-test override is obsolete for supported gameplay. |
| `docker/`, `scripts/`, `infra/`, `.downloads/` | Empty historical directories; retain locally. |
| `backups/` | Backups; retain privately. |
| `docs/provenance.md` | Historical provenance review; preserve locally, including existing attribution. |
| `.env`, `*.private.cfg`, `secrets.cfg` | Private environment/overrides; never publish. |

No game assets, compiled mods, third-party source or licenses are added here.
Existing local assets and notices are preserved; hashes verify identity, not
redistribution rights. Only the obsolete tracked `config/promod.cfg` is removed
after checking that shared plus Promod settings reproduce all nine original values.

# CoD4 server configuration

Canonical repository: https://github.com/ghptc/cod4-config-server

`config/promod.cfg` is the complete public Promod configuration: server defaults,
Search and Destroy, `match_mr12_pb`, downloads, and the four-map rotation. Keep
`sv_pure "1"`. No additional server or rotation file is needed for this mode.
Other modes have no configuration here until supported.

`cod4x-server` owns the engine, bots, administrative commands and compatibility
fixes. `ec2-workspace` owns builds, Docker Compose, SSH, deploys, rollbacks and
environment lifecycles. This repository contains no deployment tooling or game
assets. Obtain licensed game files and separately authorized mod assets outside
this checkout; configuration does not grant redistribution rights to them.

## Consume an exact revision

In a clean consumer checkout, fetch the canonical repository and check out a
reviewed full commit SHA in detached HEAD mode:

```sh
git clone --no-checkout https://github.com/ghptc/cod4-config-server.git cod4-config
cd cod4-config
git checkout --detach <reviewed-full-commit-sha>
git rev-parse HEAD
```

Package `config/promod.cfg` from that checkout. The existing `ec2-workspace`
consumer copies it to `mods/pml220/canonical-promod.cfg`, selects the active mod
with `+set fs_game mods/pml220`, and loads `+exec canonical-promod.cfg` before
starting a map. Keep runtime credentials in a separate private configuration,
loaded afterward. Record the commit SHA and configuration hash with the artifact.
Do not use this checkout's historical local Compose files for canonical builds.

## Local material retained after cleanup

The explicit ignore rules preserve the historical installation without publishing
it. No local assets or directories were deleted or moved.

| Local paths | Classification and disposition |
| --- | --- |
| `config/server.cfg`, `config/server.example.cfg` | Redundant local configuration; candidates for archiving after runtime migration. Public settings already exist in `promod.cfg`; the local server file also enables temporary diagnostics. |
| `compose.yaml`, `compose.promod.backup.yaml`, `compose.pure-test.yaml` | Deployment orchestration; retain locally for review in `ec2-workspace`. Main and backup Compose files are identical; the test override disables purity and is obsolete for supported gameplay. |
| `scripts/`, `docker/`, `infra/`, `.downloads/` | Empty historical directories; retained locally. |
| `tools/`, `assets.json` | Integrity/build tooling and asset fingerprints; retain locally pending ownership review in `cod4x-server` or orchestration review in `ec2-workspace`. |
| `game/mods/` | Required private mod assets; redistribution rights and exact provenance are unverified. |
| `game/home/`, `artifacts/` | Generated runtime state, logs and game-derived integrity artifacts; private, retained locally. |
| `backups/` | Historical configuration and Compose backups; retain locally. |
| `.env` | Private installation paths/environment; retain locally. |
| `docs/provenance.md` | Superseded historical publication review; retain locally as evidence, not current operating instructions. |

No compiled mods, extracted game scripts or third-party license material are
published by this cleanup. Existing private provenance and attribution files
remain in place. Review any proposed new configuration for credentials before
staging it; ignore rules cannot detect secrets embedded in an otherwise public file.

## Pending workspace integration

In `ec2-workspace`, update `PROMOD_REPOSITORY` in `scripts/common.sh` and the
configuration link in `README.md` from `ghptc/cod4-promod-server` to
`ghptc/cod4-config-server`. Preserve the `config/promod.cfg` packaging contract.
Its current resolver checks out a resolved master SHA and records it; accepting
an explicitly reviewed configuration SHA would also allow rebuilding an older
configuration independently of the current master. These changes belong in a
separate workspace review. No sibling repositories were modified here.

