# Verify SpecPair on Stable Studio

AI-assisted open-source prototype. Network: Studio61999; contract: 0x34d2DF8E89d7B5817412D5645104fb8DD6c113B4.

## Read the completed public record

1. Open https://complexinde.github.io/spec-pair/ .
2. Paste 0x34d2DF8E89d7B5817412D5645104fb8DD6c113B4 into Actual contract address.
3. Enter SpecH1022A as Unique record ID and click Read record. No wallet is needed for this read.
4. Expect CONFIRMED, revision2, certificate fe373cf481604198c66adc3100637652bb525b3180e9ceae16164fe6dc74fae8, two matches and total cost2. L1→R2 and L2→R1 each cost1; L3/R3 are unmatched. The displayed record contains the frozen public source snapshots and policy.

## Reproduce with a separate new test record

Use an unused ASCII record ID beginning with a letter (maximum24 characters), a test wallet on Studio61999, and the following immutable inputs. Do not reuse the completed record ID for a new Open.

Left URL: https://raw.githubusercontent.com/complexinde/spec-pair/6ffb9c8cebc523e71923122608d53b57aa5d0c77/profile07/projects/spec-pair/fixtures/left.json
Left SHA256: 89f2fef86f9c982842c99b414142316f4356858018367ac1473c10662f11281f

Right URL: https://raw.githubusercontent.com/complexinde/spec-pair/6ffb9c8cebc523e71923122608d53b57aa5d0c77/profile07/projects/spec-pair/fixtures/right.json
Right SHA256: 039bb98356382cc978ab09f35c87b01da4adc58db43fc7f0e69a59fec5e716f7

Policy: {"value_tolerance":1,"tick_tolerance":0,"value_weight":1,"tick_weight":1}

Connect the intended wallet. Open freezes the two sources and policy. After the original transaction finalizes and OPEN revision0 is loaded, Derive produces the exact result and certificate at revision1. Owner confirm uses that exact certificate and revision1 to reach CONFIRMED revision2. Every action sends value0; any test-network fees are shown by the wallet. Review wallet safety alerts yourself; no security setting was changed or warning bypass automated in the recorded validation.

If an outcome is unknown, retain the original intent/hash and use Observe same transaction; never click the write again as recovery.

## Exact recorded transactions

- Open: 0x289bf8502ddd51235bc3588705bc5f4a5d4884ed2a79466a04d8c0e7404a038c — [proof](evidence/live/open.json)
- Derive: 0x67a1c5206b4a6fddc842c9c2014bd7a18ff0827779d3f85d83be88d577eb668b — [proof](evidence/live/derive.json)
- Confirm: 0x06be650471a4fc7f150c4d4888913b56291ba2f4efe994afc5cea31039d5cb17 — [proof](evidence/live/confirm.json)

The public proof contains selected binding/finality/leader fields, not server node configuration or credentials. The source datasets are synthetic declared records. This is a validation by one operator, with no claim of independent adoption. Revoke was locally tested, not exercised in this live main path.
