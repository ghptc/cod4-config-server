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
