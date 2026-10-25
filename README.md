# CoD4 Promod Server

Promod configuration and reproducible verification of authorized external inputs.
CoD4x engine implementation and bot integration belong to `cod4x-server`.
Source resolution, packaging and Docker operations belong to `ec2-workspace`.
No engine, deployment orchestration or third-party game assets are included.

## Local preparation

Use Python 3. Obtain a licensed CoD4 installation and separately authorized
Promod LIVE V2.20 EU assets. The acquisition source and exact source-to-binary
build mapping remain unverified; this repository does not yet reproduce the
Promod fastfile from source. Do not substitute an arbitrary current upstream build.

Place authorized inputs in `game/mods/pml220` and the eight existing administrative
headers in `artifacts/integrity/addiwdheaders`. Run from this checkout:

```sh
python3 tools/verify_assets.py --root .
```

The verifier reads files only and compares all pinned external inputs. Hashes
establish identity, not redistribution rights. Do not commit these inputs.
Use `config/server.example.cfg` as a template in a separate private runtime;
add credentials there. Keep `sv_pure=1`. Existing `config/server.cfg` and compose
files are private local installation data and must remain unchanged.

`ec2-workspace` currently resolves these sibling paths directly; alternatively
set `COD4_PROMOD_ASSETS` and `COD4_INTEGRITY_HEADERS` to their absolute paths.
No obsolete PoC directory is required for those inputs. This review neither ran
packaging nor contacted EC2. Engine and bot source resolution remains owned by
that workspace. Its existing local configuration mount is not changed here.

## Reproduction limits and rollback

The installed assets are fingerprinted, not built or gameplay-tested here.
The 333 FPS source, patch, baseline, tool revisions and build procedure have not
been identified. Do not claim 333 FPS support or replace `mod.ff` until those
inputs, permissions and gameplay evidence are available. No extracted game
scripts are published. Custom script ownership is not yet established.

Preparation leaves all runtime assets and data in place. To roll back adoption,
continue using the original private configuration and asset directories; no
service or runtime change is necessary. See `docs/provenance.md` before publishing.
