# SpecPair

Globally reconcile two declared record lists, maximizing admissible one-to-one matches before minimizing exact integer mismatch cost.

**AI-assisted experimental local prototype.** This is one complete original Project (contract + distinct interactive frontend + synthetic fixtures + tests). Its bundled contract is not an extra independent IC contribution. No LLM is used. No deployment, public source, hosting, live wallet business flow, real user, funding or award is claimed.

## Deterministic domain

Sources are strict version1 lists of0..8 records each, with unique ASCII IDs, exact category/unit IDs, integer value±1000000 and abstract tick0..1000000. Locked policy has value_tolerance0..2000000, tick_tolerance0..1000000, value_weight1..1000 and tick_weight0..1000. Admissible pairs agree on category and unit and meet both tolerances; cost is weighted absolute value/tick difference.

ASCII-sort IDs on each side. Suffix bitmask dynamic programming minimizes (-matched_count,total_cost,assignment_vector), using right ASCII index and len(right) as the unmatched sentinel. This exhaustively considers at most8*256 states. The result includes the complete cost/rejection grid, pair deltas/costs and both unmatched lists. Both empty sources produce EMPTY; otherwise a zero-cardinality optimum is NO_MATCH. These are meaningful abstract outcomes, not a claim real objects are absent.

The original fixture deliberately defeats greedy first-pair choice: L1→R2 and L2→R1 give2 matches at cost2, vector[1,0,3]; L3 and R3 remain unmatched. The manual pairing panel demonstrates duplicate-right/admissibility conflicts and compares its objective without submitting a proposed answer.

## API and state

Constructor: **zero arguments**. Each open record is owned by its caller; the deploying account has no exclusive registration privilege. Record IDs are globally first-writer and never reusable. Choose a fresh ID and inspect its actual owner; this is not an identity/namespace ownership service.

| Method | Behavior |
| --- | --- |
| `open_pair(record_id,left_url,left_sha256,right_url,right_sha256,policy_json)` | Immutable URL/byte hashes/policy, independently verified source; OPEN revision0. |
| `derive_pair(record_id,expected_revision)` | Permissionless, one fresh full computation; DERIVED revision1 and bound certificate. |
| `confirm_pair(record_id,expected_revision,certificate_id)` | Original owner only; exact current certificate/CAS and another fresh full computation; CONFIRMED revision2. |
| `revoke_pair(record_id,expected_revision,reason)` | Original owner only, trimmed reason1..160; terminal from any unrevoked stage; no network needed. |
| `get_pair(record_id)` | Actual decoded dictionary with owner, source snapshots, result, certificate, captures and finite history. |
| `get_configuration()` | Actual decoded dictionary with protocol/resource limits. |

At most four history entries per record: OPEN/DERIVED/CONFIRMED/REVOKED. Revoked results remain visible as historical and cannot be reactivated. Failed source/validation writes preserve prior state. No funds are held or transferred.

## Independent source consensus

Canonical public source locators require HTTPS raw.githubusercontent.com/owner/repo/40-lowercase-hex/path, explicit segment checks and lowercase SHA256. Dot/empty/encoded segments, queries and mutable refs are rejected. HTTP200,1..16384 exact UTF8 bytes, SHA256, strict unknown/duplicate-key/nonfinite/type/size schema validation are mandatory. The size bound is post-download, not a network bandwidth or redirect control. Availability, GitHub transport and source-author truth remain assumptions.

During open, derive and confirm, every validator independently fetches every original locator, validates bytes and schema and recomputes the complete binding/source/result packet. Full canonical equality rejects valid-looking but suboptimal/noncanonical proposals; tests include such complete forged packets. Binding includes protocol, chain, contract, owner, record, locators/hashes, policy, revision, operation and observation time. Revocation deliberately requires no source availability. See THREAT_MODEL.md.

## Reproduce local evidence

Use Python3.12 and exact requirements, Node20.19+/22.12+ and pnpm11.25.0. Run from this individual package directory because gltest clears its cwd artifacts folder:

```powershell
python -m venv .venv
# Activate the local venv.
python -m pip install -r requirements.txt
python tools/verify.py
cd frontend
pnpm install --frozen-lockfile
pnpm test
pnpm build
pnpm dev
```

`tools/verify.py` uses the exact GenVMv0.2.12 runner pinned in contract.py, actual genlayer-test0.29.2 storage/calldata/validator execution, genvm-linter0.11.0 full semantic validation/schema and zero constructor parameters. The narrow Windows compatibility fixture only handles upstream fd0 temp-file cleanup/warp metadata; it does not replace contract computation. HTTP responses are explicit test fixtures. No direct test is a network transaction.

Recorded final suite: **30 actual SDK tests and 56 frontend tests**, full semantic/schema/TypeScript/Vite exit0. `evidence/sdk-initial-red.log` records the minimal no-behavior skeleton failures; frontend assertion stubs and missing UI behavior red logs are retained. Frontend tests execute production domain/wallet/actual-main handlers; transports/DOM are controlled harnesses. The Vite actual SDK bundle exceeds500kB before compression, a retained nonfatal notice. `python tools/verify_frontend.py` reproduces checks and exact frontend input hashes.

## Configure the real workflow

Fixtures are original MIT synthetic examples, not actual customers or external facts. Every test_url in fixtures/source.json is a local mocked locator; **all public_url fields are null**. Publish exact source bytes at real immutable commits and independently verify the digests. Policy.json in SpecPair is a constructor-free open parameter fixture, not a third fetched source. Enter actual published URLs/hashes, an independently verified zero-argument deployment address on Studio61999 and a unique record ID.

Connect MetaMask → open immutable sources → derive → inspect the actual loaded result and witnesses → owner confirm the exact certificate, or separately revoke. Local editors and JSON exports do not publish, deploy or update chain state. Edited local previews clear the loaded confirmation context; only a verified source/result read can enable confirmation. Source-only previews are labeled local computation, and revoked overlays are labeled historical.

The actual genlayer-js2.0.0-rc.2 adapter matches these dictionary views. It requests fullTransaction finalized observation and mandatory independent unformatted eth_getTransactionByHash proof of the original hash/from/to/value0, FINALIZED/NORMAL/leader_only=false/MAJORITY_AGREE and exactly one leader SUCCESS. Every available SDK binding/status/execution field must agree; named/numeric execution contradictions and unknown numeric codes fail closed. Missing Studio fields stay missing. Actual SDK helper/viem formatter tests use a captured public constructor reference from another contract; this is not this Project live business evidence.

Before SDK submission, public original account/contract/record/method/hash-null metadata is saved in session storage. Network errors, invalid/missing hashes and failed/unknown execution block another write. Only explicit wallet rejection code4001 clears a hashless attempt. Same-tab reload restores the context; reconnect the original account, attach only its original wallet-activity hash if needed and choose Observe same transaction. Attaching a hash does not reconstruct lost calldata independently. Observation never resubmits. Removing storage, a different tab/origin or unavailable storage defeats a browser-local guard; retain original wallet activity/hash independently. No keys or secrets are stored.

Busy operations disable all controls; captured address/record epoch and final visible-context checks discard stale reads/actions even if disabled inputs are changed programmatically. The UI is original domain functionality, not a substitute for chain results. Browser visual QA and full actual wallet/network business flow remain unverified.

## Release status

MIT licensed. PUBLISH_MANIFEST.json binds the complete allowlisted payload; dependencies,SDK caches,build output,environment files and credentials are excluded. CONTRIBUTION.json counts this once as a Project. Independent local peer review is closed with no Important/Critical finding; the reviewer read source, recorded evidence and archives without rerunning full SDK/frontend suites. This is not an external audit. Public source publication, deployment, hosting and real business verification belong to the root task. Exact contract SHA256: 135f33e7a0eb1e1da4de08f78d7d0bb6ea8029829379b150a1803d959cf6e1ae.

The exact reviewed pre-finalization ZIP is preserved in the workspace history directory. Final source-only reseal adds peer evidence and metadata only; contract and frontend input hashes are unchanged. See evidence/independent-review.json and independent-artifact-check.json.
