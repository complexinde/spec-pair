# Trust and threat boundaries

This is an AI-assisted local prototype, not an audit. Public synthetic structured data is untrusted: byte/hash/schema checks precede computation and every validator independently refetches/recomputes. No LLM/prompt execution is used; imported strings enter UI textContent, never external HTML. Resource bounds constrain computation after download, not HTTP transport. Content hash does not authenticate the publisher or prove real-world claims.

Consensus certificate binds protocol/chain/contract/owner/record/immutable source hashes/policy/revision/time and the complete canonical result. Source drift, malformed input, leader fabrication, nonoptimal/canonical tie substitution and transient outage must fail closed. Local direct tests execute actual SDK state and validator callbacks but do not establish deployed multi-validator behavior or gas cost.

Owner-only exact-revision/certificate confirmation and terminal revocation prevent takeover/replay of existing records. IDs remain first-writer global and public; choose a unique ID and inspect its owner. History is finite per record; there is no claim of a globally finite record registry or protection against all registration spam. Revocation is offline; old results are historical, not active authority.

Frontend is a cooperative local guard, not network-wide exactly-once execution. It persists public original context before broadcast, observes unknown transactions without resubmission and requires raw consensus success/identity proof before reads. Explicit manual missing-hash attachment relies on the user choosing the original wallet activity, not an unrelated successful call. Session storage loss/cross-origin or compromised RPC/browser/wallet are outside that guarantee. Wallet secrets are never requested or stored. No real funds, personal identities, physical work, booking authority or safety decision is entrusted to this prototype.

Browser rendering/visual QA, public fixture availability, real chain deployment and complete live business workflow are not verified.
