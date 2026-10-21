# SpecPair

SpecPair is an AI-assisted, MIT-licensed prototype that compares two declared synthetic observation tables. GenLayer fetches exact commit-pinned public inputs, freezes the declared policy, derives a canonical maximum-cardinality/minimum-cost pairing, and records an owner-confirmed certificate. It does not identify real people or claim real-world truth.

## Current frontend and recorded live demonstration

The application is [https://complexinde.github.io/spec-pair/](https://complexinde.github.io/spec-pair/). The existing contract is `0x34d2DF8E89d7B5817412D5645104fb8DD6c113B4` on **GenLayer Studio, chain61999**. Current frontend revision**004** is a reviewed display/error/receipt-consistency update. Its local checks are **153 frontend tests**, **30 pinned contract SDK tests**, and TypeScript/Vite exit0. Its fresh [independent peer review](evidence/frontend-revision004/independent-review.json) is **PASS_WITHIN_REVIEWED_SCOPE**, with no outstanding Important/Critical findings in that stated scope. See [FRONTEND_REVISION_004.md](FRONTEND_REVISION_004.md), the [verification report](evidence/frontend-revision004/revision-verification.json) and [LIVE_STATUS.json](LIVE_STATUS.json) for exact source/build/peer hashes and snapshot boundaries.

The genuine Open -> Derive -> Owner confirm demonstration was performed with frontend revision**003**, commit `a92917262bc5cd210346630bea1c5f7aa24aec2a`. Record **SpecH1022A** reached **CONFIRMED, revision2**, certificate `fe373cf481604198c66adc3100637652bb525b3180e9ceae16164fe6dc74fae8`. All three original business transactions were FINALIZED with NORMAL consensus, MAJORITY_AGREE and one successful leader. This existing result remains valid. No new wallet main workflow or duplicate business transaction is claimed for revision004; public asset verification and a read-only check of the existing record are recorded separately.

The exact result matches **L1->R2 and L2->R1**, with two matched pairs and total cost2; L3 and R3 remain unmatched under the declared synthetic policy. Inspect the **Admissibility and exact cost grid** section and the recorded source/result/certificate for the explanation.

| Demonstrated revision003 transition | Original transaction hash |
| --- | --- |
| open_pair | `0x289bf8502ddd51235bc3588705bc5f4a5d4884ed2a79466a04d8c0e7404a038c` |
| derive_pair | `0x67a1c5206b4a6fddc842c9c2014bd7a18ff0827779d3f85d83be88d577eb668b` |
| confirm_pair | `0x06be650471a4fc7f150c4d4888913b56291ba2f4efe994afc5cea31039d5cb17` |

See [LIVE_WALKTHROUGH.md](LIVE_WALKTHROUGH.md) and [the immutable main-workflow evidence](evidence/live/main-workflow.json). Those original evidence files remain dated revision003 snapshots. Their earlier Portal submitted=false fields describe that earlier time and do not override the current submission snapshot below.

## Read the confirmed record

1. Open the public application. A read-only visit needs no wallet connection or signature.
2. Fill **Actual contract address** with `0x34d2DF8E89d7B5817412D5645104fb8DD6c113B4`, set **Unique record ID** to `SpecH1022A`, and click **Read record**.
3. Expand **Loaded source, result and certificate**; verify CONFIRMED/revision2 and the certificate above, then inspect the domain result and witness. Compare the original hashes against the immutable evidence. This walkthrough does not ask a reader to repeat a transaction.

## What revision004 changes

The public notice/trail uses a fixed UNVERIFIED diagnostic instead of echoing arbitrary provider/RPC errors. Changing record, address, account or chain clears the prior displayed public receipt; a plain read also clears it, and stale callbacks do not restore it into another context. Explicit SDK leader-receipt lists must contain exactly one successful leader: empty/validator-only lists fail closed. Independently bound raw finality/majority/leader proof remains mandatory, and missing SDK fields are not invented.

Contract source, fixtures, domain algorithms, dictionary ABI, pending storage schema, exact-hash recovery, official genlayer-js1.1.8 serializer/checksum boundary and the one-shot wallet mutation gate are unchanged. Unknown submissions retain their original context/hash and must never be automatically resent. There is no wallet-warning bypass.

One nonblocking presentation limitation remains: **A previous verified receipt for the same record may remain visible if a later action becomes UNVERIFIED/unknown. That receipt is historical evidence only and does not prove the new action succeeded. The pending original context/hash still blocks replay; record/address/account/chain changes and plain reads clear the displayed prior proof.** This is not a claim that all historical proof disappears or that an unresolved new action succeeded.

## Current scope and Portal snapshot

At snapshot **2026-10-21T19:04:48.625558+00:00**, the existing SpecPair Project submission is **Pending review**, visible ID prefix **daf36dab**, submitted=true and accepted=false. The observed submission timestamp is `2026-10-21T18:02:21.299Z`. This update did not submit again; Pending review is not acceptance, an award or guaranteed points.

The demonstrated use is synthetic and operated by one wallet user. Revoke is implemented and locally tested, but was not exercised live. No independent adoption, production use, real-world identity/scheduling, funding or award is claimed. The contract source remains SHA256 `135f33e7a0eb1e1da4de08f78d7d0bb6ea8029829379b150a1803d959cf6e1ae`; the original constructor transaction remains `0x546f0c8c2414bd22d1ebb1211f5602287e8d80269c85bddcca0c757a6d1f0560` and is separate from the business hashes above. [deployment.json](deployment.json) keeps the actual published constructor schema and values.

[HISTORICAL_README_FRONTEND003.md](HISTORICAL_README_FRONTEND003.md) preserves the exact README from verified public commit `d4178b03570b271a3bee6f17b0405497de5fa23f`. It is historical; the current status is the timestamped, scoped metadata above. The original public inputs and existing evidence files are unchanged by this frontend update.
