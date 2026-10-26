# CoD4 configuration catalog

Canonical repository: https://github.com/ghptc/cod4-config-server

Only Promod LIVE 2.20 is implemented. The engine and private script preparation
belong to `cod4x-server`; packaging and startup argv belong to `ec2-workspace`.
Private assets, credentials and historical local installations remain ignored.

## Ownership and startup

- `shared/server.cfg` supplies defaults. Private CFGs supply credentials and
  permitted environment overrides, such as the download base URL. Original
  Promod competition rules still enforce their voice/download settings. Purity
  remains 1; filesystem selection belongs to startup metadata.
- `modes/<id>/mode.cfg` contains only literal startup `fs_game` metadata.
- `modes/<id>/server.cfg` owns every setting it declares: mode identity, capacity,
  gameplay, rotation and voting. Private CFGs cannot override those settings.

Consumers validate the catalog, package immutable `canonical-shared.cfg` and
`canonical-mode.cfg`, and start with filesystem/capacity arguments, followed by
shared CFG, private CFGs in their existing relative order, then mode CFG, then
native `+map_rotate`. The final mode CFG intentionally supersedes obsolete
private gameplay overrides. No manual CFG reload is required. `+set` is processed
early by the engine; it is not a late override mechanism. A mode-owned capacity
conflict in argv is rejected before launch. Private files are never rewritten.

Promod enables native human-only next-map voting and randomized rotation across
all 21 installed base-game map scripts with pinned Bot Warfare waypoints.
Packaging must verify each selected map against the prepared asset manifest;
installations missing a map must fail qualification rather than shorten the
rotation silently. This is asset/script coverage, not certification of every
map's competitive balance, navigation or bomb objectives.

The companion engine preparation must enable `--allow-map-voting`, which removes
only Promod's original competition voting prohibition. Bots satisfy the original
Ready Up loop after selecting a playing team and class; human use-button and
recording checks remain. Ready Up is enabled, not bypassed. Completed matches
exit through native rotation; individual S&D rounds still restart the same map.
Passed player votes select the next map before shuffled rotation resumes.

## Catalog validation

Use a clean exact reviewed commit. Discover all immediate `modes/` directories
in byte order; IDs match `[a-z][a-z0-9-]*` with no aliases/fallbacks. Reject
symlinks, malformed/incomplete directories and unknown selected IDs. Require
nonempty regular `shared/server.cfg`, `mode.cfg` and `server.cfg`.

The native CFG subset is blank lines, full-line `//` comments and one literal
`set name "value"` per line. Reject duplicate keys, credentials, commands, quotes,
backslashes, semicolons and controls in values. `mode.cfg` contains exactly
`set fs_game "mods/<directory>"` (or an empty value for a qualified base mode).
Filesystem settings are forbidden in shared/gameplay files. Shared/mode overlaps
require `// Override shared: <setting>`. Validate purity, capacity (1–64), required
identity/gametype/rotation, and groups `gametype <name> map <name>` with the first
gametype matching `g_gametype`. The first map is metadata, not a forced startup
map when shuffled rotation is enabled.

Record mode ID, exact configuration/engine/dependency revisions, all three CFG
hashes, asset hashes and immutable artifact identity. Validate selected authorized
assets only; never assume a future mode supports Promod transformations. Mode
switching requires an explicitly qualified artifact and owner-controlled review.
Production approval, deployment and rollback remain outside this repository.
Removing a catalog mode does not change an already packaged artifact.

Historical `config/`, `game/`, `backups/`, `artifacts/`, Compose files and local
tools are preserved privately under existing ignore rules. No game assets,
extracted scripts, binaries or credentials belong in this repository.
