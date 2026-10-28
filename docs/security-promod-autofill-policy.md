# Security release: preserve the private Auto-Fill policy

A read-only production `bot_status` check on 2026-10-27 found Auto-Fill disabled,
with limit12. The first pinned security image used catalog9f0fa1a, whose final
Promod rules forced `bot_enable "1"` after private configuration. Deploying that
image would enable an unrelated gameplay policy during the security freeze.

Remove the final forced enable directive. Shared defaults and final mode rules
now leave the private/operator choice intact. The reviewed native engine defaults
Auto-Fill off, so no private enable directive also remains off. Explicit private
enabling and existing administration commands retain their normal authority.
Capacity, the fill limit, map rotation and integrity policy are unchanged.

The regression checks model the documented shared → private → final-mode order.
They fail against9f0fa1a for both the off default and an explicit private off
choice, and pass after this change; an explicit private on choice also survives.
Actual runtime confirmation still requires rebuilding with the new approved
config revision and querying the isolated/homolog candidate.

This PR changes no running service, secret or production file. The previously
built image remains preserved and is not edited or promoted. After owner review,
mandatory CI and a manual merge, bind a reviewed preparation driver to the exact
new config commit, rebuild through that driver, verify the new image/CFG hashes
and requalify the affected runtime behavior. Do not reuse the old image's approval
or substitute configuration under its digest. Homologation deployment and any
production release require separate explicit operator approval.
