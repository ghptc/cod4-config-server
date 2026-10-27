# Zombies native map voting

Enable existing native voting for `/callvote map mp_crash` (select next map)
and `/callvote map_rotate` (switch through the existing engine transition).
Only rotation maps are accepted. `/callvote map mp_killhouse` is now eligible;
Killhouse is appended after the original 15 maps, with `war` throughout.
District (`mp_citystreets`) and unknown maps remain rejected. The existing
human-only voting, quorum, cooldown and vote limits remain enabled.

Killhouse requires the reviewed pinned navigation preparation from
[engine PR #23](https://github.com/ghptc/cod4x-server/pull/23) and packaging contract
[workspace PR #16](https://github.com/ghptc/ec2-workspace/pull/16), both merged into
protected master. Homolog artifact `sha256:9aa4247e7ff9b1bd2c03266f18b8ee7b7a168bafa3c8b68412059be150bc98f8`
was inspected read-only: its navigation overlay SHA-256 is
`10fb2268d2ea64c14d0a7040e180151265a4b2827ebc44068e82831a18ff9c56`, matching
the preparation manifest; its active catalog still contains the original 15 maps.
[Engine PR #24](https://github.com/ghptc/cod4x-server/pull/24) must also be
merged to declare repaired Killhouse in the prepared asset map list. Without it, packaging correctly rejects this catalog. Never edit
private manifests or vendor assets to bypass that gate.

After green mandatory CI, independent review and operator-approved merges,
prepare/deploy only through the existing homologation workflow. Do not merge or
deploy automatically. After deployment, require real-client navigation, combat,
waves, death, respawn and stationary/elevated camping tests before declaring
Killhouse qualified. Native synthetic-client evidence does not replace this gate.

Zombies mode sets configurable `g_voteCooldown=5`, `g_voteTime=30`,
`g_voteMaxVotes=2`, `g_voteAbstainWeight=1`. Kick, restart and gametype votes
are disabled. The engine excludes bots from calling, casting and quorum.
Promod configuration is unchanged; no wave globals are manipulated by this change.

Baseline config master: `9fd5c9d`. Catalog policy test and 22 discovery contract
tests passed. Companion engine native vote/rotation tests passed. Local BTD
integration passed 89/89 checks across 15 supported maps and process restart:
`/tmp/cod4-btd-qualified-18naigad`. This checks policy, map startup, purity,
eight integrity headers and absence of script errors. It does not certify
real-client vote UI or vote-driven transitions during combat.

Additional local evidence: BTD lifecycle passed with the proposed policy at
`/tmp/btd-death-regression-uh2phcph` (death, respawn, wave two, admission and
administrative map transitions). Fresh pinned Promod overlays passed 53/53
integration checks at `/tmp/cod4x-promod-integration-6yoxi62_`, including ready-up,
voting and administration. An older prepared runtime failed ready-up checks;
its overlay differs from current preparation and is retained as historical evidence.

Keep `bot_enable=0` until a separate BTD ally adapter is implemented and qualified.
Require independent review, green mandatory Configuration tests and owner merge.
Operator-supervised gameplay and explicit approval remain necessary for deployment.
Rollback by reverting this focused policy change through the existing reviewed
workflow. No running service was changed.


## Killhouse activation verification (2026-10-27)

Configuration policy and all 22 workspace catalog/packaging tests pass. Exact
native handler tests using this catalog accept each of the 16 maps and reject
District, unknown names, partial names, injection/path inputs and bot callers;
existing cooldown/quorum protections also pass. All settings except the appended
rotation entry are unchanged. Shared and Promod configurations are byte-identical.

Private generated preparation and workspace packaging pass with engine PR #24.
BTD integration passes 73/73 checks across the original 15 maps, Killhouse and
restart (`/tmp/cod4-btd-qualified-5r_ixsre`); Promod passes 53/53
(`/tmp/cod4x-promod-integration-1v8iw1em`). Engine unit suite passes 60 tests
with one skip; native rotation and voting suites and mocked operations pass.
Final native Killhouse regression passes 12/12
(`/tmp/btd-navigation-w7ngrvsr`): 101 nodes, 25 linked spawns, pathing, chase,
melee, bullet combat, wave progression, respawn, camping and map transitions.
BTD lifecycle also passes (`/tmp/btd-death-regression-a2gi__hy`), including
death, respawn, wave progression, admission and administrative transitions.
Independent agent review found no code blockers in either PR and independently
reran all 12 preparation tests. Full logs, private assets and disposable test
fixtures stay outside these PRs. Synthetic clients and accelerated fixtures
remain local regression evidence only.

## Operator-only homologation command

After both PRs pass mandatory CI and the operator approves their manual merges,
run from the reviewed workspace checkout in an interactive terminal. The existing
workflow fetches clean canonical engine/configuration master checkouts, rebuilds,
validates and targets only homologation. The explicit original private inputs
below existed and passed hash verification during this session; if relocated,
provide their verified original paths instead. Do not substitute a prepared
runtime for the original BTD package.

```bash
cd /home/gabriel/Projects/ec2-workspace
COD4_BTD_ASSETS='/tmp/cod4-btd-package/Before The Dawn Alpha 001' \
COD4_INTEGRITY_HEADERS='/tmp/btd-killhouse-nav-prepared-20261027/integrity/addiwdheaders' \
./scripts/deploy-homolog.sh zombies
```

This command is prepared, not executed. Keep the existing rollback baseline.
Do not approve the candidate until a real client has tested navigation, combat,
wave progression, death, respawn and stationary/elevated camping on Killhouse.
Confirm `/callvote map mp_killhouse`, unsupported-map rejection and the original
15 maps on the deployed image. Record the exact new image digest, source/config
SHAs, client results and operator approval. Do not promote to production.
Revert the focused configuration commit and rebuild through the same reviewed
workflow if the catalog change needs rollback; never rewrite private assets.
