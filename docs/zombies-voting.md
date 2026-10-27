# Zombies native map voting

Enable existing native voting for `/callvote map mp_crash` (select next map)
and `/callvote map_rotate` (switch through the existing engine transition).
Only rotation maps are accepted. Killhouse remains excluded; native BTD startup
fails in its waypoint loader and supervised gameplay is not qualified.

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
