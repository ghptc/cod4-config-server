# CoD4 configuration catalog
<table>
  <tr>
    <td width="160" align="center">
      <img
        src="assets/nvg-star-emblem.gif"
        alt="NVG Star Emblem"
        width="130"
      />
    </td>
    <td>
      <p>
        Canonical repository:
        <a href="https://github.com/ghptc/cod4-config-server">
          ghptc/cod4-config-server
        </a>
      </p>
      <p>
        Promod LIVE 2.20 is implemented. Before the Dawn Alpha 001
        has a separate Zombies configuration candidate, qualified
        for local startup but not yet for combat or artifact promotion.
        The engine and private script preparation belong to
        <code>cod4x-server</code>; packaging and startup argv belong
        to <code>ec2-workspace</code>. Private assets, credentials
        and historical local installations remain ignored.
      </p>
    </td>
  </tr>
</table>

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
only Promod's original competition voting prohibition. Only eligible human players contribute to Ready Up; bots are excluded and a
bot-only lobby waits for a human. Human use-button and recording checks remain.
Ready Up is enabled. Completed matches
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


## Before the Dawn Zombies candidate

`modes/zombies/mode.cfg` selects the original `mods/btd_alpha_001` directory;
`server.cfg` selects `war`, preserves the original 15 maps in order and appends
Killhouse using the reviewed navigation preparation. District remains excluded.
Killhouse requires real-client homologation qualification before it is qualified. Player capacity
is explicitly 12; zombie counts are the mod's own wave policy, not
Promod Auto-Fill. `bot_enable=0` prevents attaching the Promod integration.
Promod retains its existing Bot Warfare auto-fill behavior with explicit mode-owned
settings. Hardcore remains unavailable until separately
registered and qualified.

The original archive SHA-256 is
`dad2e94a92823844ab411f3dfadd0f2dacc491b9df3416db8b1a1f9fb9f4d410`.
Private inputs are original `mod.ff`, `btd_images.iwd`, `btd_music.iwd`,
`btd_weapons.iwd` and the vendor CFGs. Engine preparation verifies all files,
preserves original bytes/notices and never decompiles the fastfile. No
redistribution grant was found in its readme; no assets or vendor CFG copies are
included in this repository.

The original sample server CFG is deliberately excluded from runtime preparation:
it embeds sample passwords, an old download URL and an exec for absent
`btd_trade.cfg`. The workspace packages verified vendor defaults into the shared
phase, then private CFGs, then this canonical mode policy. Original admin identity
settings belong in a private CFG. Music stays disabled by canonical policy.
There is no nested exec or filesystem selection in the gameplay CFG.

Local real-engine startup checks cover all listed maps, purity, header loading,
private conflicts and fresh processes. Actual native zombie combat, client asset
loading and container transitions remain qualification gates. Catalog discovery
is not homologation or production authorization. The engine `change_mode`
preflight currently reports all activation targets unavailable and changes
nothing; no privileged RCON control channel is enabled.

Current workspace image building remains intentionally limited to Promod. Its
separate BTD private packaging support does not enable image promotion, downloads,
builds or deployments from RCON. See the engine RCON investigation for exact
hashes, original-package findings, test limits and rollback. To revert this
candidate, revert its catalog commit; existing packaged Promod artifacts retain
their exact configuration and identity.

The candidate passed 53 local engine startup/map/preflight checks, including all
15 configured maps and the private `sd` versus canonical `war` conflict after the
companion generic string-latch correction. Evidence:
`/tmp/cod4-btd-qualified-biebk8zp/results.json`. The unchanged Promod policy passed
53 independent real-runtime checks. No combat/homolog approval is implied.


## Required CI

`Configuration tests` runs on hosted GitHub CI for PRs and pushes to master. It
uses the existing workspace catalog validator at exact revision
`37f83f6927c93a10a078fb4748c37e52d42f8e5a`; no private assets are needed. The active
[master ruleset](https://github.com/ghptc/cod4-config-server/rules/25857702)
requires this GitHub Actions check with an up-to-date branch and no bypass actors.
Local tests alone do not establish branch protection. See the workspace
restoration report for live CI evidence and Zombies real-client blockers.

## Zombies Classic policy

The canonical Zombies CFG sets the existing `btd_anticamp` option to `0`.
The verified Alpha 001 timer dispatcher runs only for `2` or `3`; its map
teleport dispatcher creates camping-spot triggers only for `1` or `3`.
Zero suppresses both, allowing stationary play and accessible elevated map
positions without timer punishment or those forced relocations. No engine
coordinate validation or other gameplay system is changed. The timer reads the
setting on player initialization and teleport triggers initialize with the map;
apply through the normal immutable startup flow and a fresh map, not a live
dvar toggle.

The existing `btd_msg2` value keeps `^7Server admins are ^4` and replaces only the
four server administrator names/separators with `pitta`. The original message
rotation, colors, timing and placement remain controlled by the shipped mod.
Original author credits and private administrator authentication stay intact.
Both settings are final mode-owned overrides after vendor and private CFGs.
Promod configuration and Zombies combat/wave balance remain unchanged.

Source inspection used the original archive identified above and the verified
plaintext raw-source members `btd_general/_anti_camp_time.gsc` and
`btd_general/_anti_camp_teleport.gsc`, plus the existing vendor
`btd_messages.cfg`. No private scripts or vendor configuration copies are
published. Engine preparation and native behavioral regression results belong
to the companion `cod4x-server` change. Real-client camping, elevated positions,
message display, combat, death/respawn, reconnection and map changes still require
supervised homologation qualification by exact reviewed image digest.

Rollback: revert this configuration commit, rebuild through the existing
workspace pipeline from reviewed master revisions and obtain operator approval
before deployment. Existing artifacts are unchanged by catalog edits.
