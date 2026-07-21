# Know-how promotion record — 2026-07

Status: no genre claim promoted; proposals remain maintainer-side.

Production-form guidance is evaluated separately and promoted; its complete
deidentified package and decision are retained under `production-form-2026-07/`.

This is a deidentified decision record over synthetic inputs. It contains no source
locator, source wording, connection detail, or media output. The record preserves
negative evidence so that a future maintainer does not mistake an anonymous-arm
preference for permission to ship a rule.

## Version evidence

Baseline revision: 15eba8d6aa89514f76fe4d659727a29565f288fc

The baseline arm used the public suite at that revision. Candidate executors used
the then-current public suite whose core manifest SHA-256 was
`7aca45340c4dc207053564136d72eeeafd7a19db571247288f516682f954a862`.
That candidate contained other cleanup changes, so package equivalence was not
proved and none of these runs can independently authorize promotion.

### Investigation / hearing run

Fixture: `fixtures/investigation-hearing.json`

Input SHA-256: db1d171ebe76cbba1ffc9342ff838fb9276619d52144393d9c29f06be9075950

Baseline output SHA-256: 21489de7da9806d2164d260e697a5d124b2647297d13ec2ff0f08518ebcb5134

Candidate output SHA-256: 578a122b53bc1e2685778ae5dcefe10f75e419aa62d852be93689def10b24bc4

Anonymous-arm SHA-256 values: Maple
`c5915743b25647e715048cf7a330a696606ed64b49e37b1ad5c45b9e4d6213b0`;
Quartz `f561bede821e02de361f2eab05e9555da159997ee6cafafec6ecaf85413d8c8a`.

### Three-genre transfer run

Fixture: `fixtures/historical-biography.json`

Input SHA-256: 29ae373727e18f073eb2576b194338172090359096d153508777abfcd42d366f

Fixture: `fixtures/competition-system.json`

Input SHA-256: 708d6d881c45acb3d7f2675803a35f743aae95f504c8c0e11be721e088ba6368

Fixture: `fixtures/labor-greenhouse.json`

Input SHA-256: 315222ca4fbcee5826a9051aae44704e85846434ccac0aef91e92a4b40f451a4

Baseline output SHA-256: 4f503ed5899f0bf3338412d3227753d58d891bbae0e96dcd1b5655e9ccb20a9a

Candidate output SHA-256: fd8f9884a8ff47f1dc416ddd4a2ac8a6d74317d046efdfb8aca0fe9d2e5d2b96

Anonymous-arm SHA-256 values: Cedar
`e2069a397f7055d5294e6442c523f44e11e7e34e5fba2f0bd193cbb4c84a188a`;
Dawn `add591124fe4d1d33722ab28d9a219d02d382d867cc18101e9f2527929bcc934`.

## Retention status

Raw arms, anonymized arms, reviewer reports, and executor prompts were kept only
in coordinator state under `.omx/evals/current/` and `.omx/evals/blind-review/`
during this run. They are **not retained in this repository** and have no durable
release-artifact locator; only the hashes and bounded findings above are retained.
The target-only candidate package and tool-call summaries were also not retained.
Consequently a future maintainer can verify the staged fixture bytes and detect a
different output, but cannot reconstruct the original comparison or re-audit its
semantic verdict from this repository alone. This retention gap is an additional
reason every claim remains unpromoted. A retry must archive deidentified prompts,
anonymous outputs, verdict, package hashes, and tool summaries in its authorized
maintainer store before requesting promotion.

## Executor provenance

- Investigation baseline: `/root/blind_eval_baseline_b`; fresh arm assigned
  only the isolated baseline skills and the neutral input.
- Investigation candidate: `/root/blind_eval_creator_b`; fresh arm assigned
  only the candidate public skills and the same neutral input.
- Transfer baseline: `/root/genre_transfer_baseline`; fresh arm assigned only
  the isolated baseline skills and three neutral inputs.
- Transfer candidate: `/root/genre_transfer_candidate`; fresh arm assigned only
  the candidate public skills and the same three neutral inputs.
- Each executor attested that it did not read the opposite arm, evaluation
  verdict, source research, or version mapping. These are declared provenance
  statements, not cryptographic proof of runtime identity.

## Reviewer provenance

- Investigation reviewer: `/root/genre_blind_reviewer`; fresh, independent,
  authored neither arm, mapping hidden until verdict. Verdict artifact SHA-256:
  `b31e0c08c5234526ebbaef5893c75d5a012fcb4317dc183354de57a6ec7d3089`.
- Transfer reviewer: `/root/genre_transfer_reviewer`; fresh, independent,
  authored neither arm, mapping hidden until verdict. Verdict artifact SHA-256:
  `76fc2b5cd7310bf3cb14aaa467852d1cfa4f8e0068064a96159546972ebbe4b6`.

## Blind findings

### Investigation

The reviewer preferred baseline arm Maple at confidence `0.74`. Quartz had the
strongest single falsifiable action—jointly checking an original record—but its
motion text introduced an unbound record and pen, conflicted with the frozen
hand state, and depended on a conveniently available original. The fixture also
announced that each evidence carrier was partial, so it tested compliance more
than discovery. Decision: `narrow-and-retest`, not promotion.

### Historical biography, competition, and labor

The reviewer preferred Dawn overall: Dawn protected an absent archive-destination
value and made the labor result conditional; competition was a tie because one
arm had a cleaner ability state machine and the other a better motion translation.
All three inputs materially cued the desired ledger. Biography still lacked a
landed payoff without inventing the missing fact, ability activation remained
ambiguous, and neither package completed every requested downstream layer.
No result reached promotion-grade incremental evidence.

An earlier urban/dialogue comparison preferred its candidate presentation but
found shot coverage and frozen-boundary defects. It was diagnostic only and did
not authorize any genre claim.

## Claim decisions

| Claim | Decision | Public outcome | Required next contrast |
|---|---|---|---|
| Investigation evidence / hypothesis ladder | `narrow-and-retest` | Investigation-specific proposal and fixture removed from the public runtime; synthetic fixture retained here | Original unavailable or contradictory; credential semantics change; negative evidence has known reliability; correct story reasoning with an injected shot-state failure |
| `STY-17` fact-confidence ledger | `narrow-and-retest` | `STY-17` and its genre prose are not in the public index | Mixed public record, disputed attribution, absent decisive value, and a required local payoff that does not invent that value |
| `STY-18` ability grammar / changed affordance | `hold` | `STY-18` and its genre prose are not in the public index | Less pre-filled trigger; distinguish involuntary signal, voluntary activation, refusal, counterplay, entry/exit state, and exact motion boundary |
| `STY-19` labor trial → validation → new constraint | `narrow-and-retest` | `STY-19` and its genre prose are not in the public index | Non-agricultural transfer plus failed/null trial where the input does not supply hypothesis, control, result, or next bottleneck |

The public asset voice binding, relationship-aware blocking, `SHT-14` dynamic-object
and prop continuity, scene-depth options, single-dramatic-change motion guidance,
and multi-image boundary clarifications are not promoted by this record. They came
from the current creator requirements and were reviewed as ordinary cross-genre
product/craft changes, not as the competition fixture's genre claim.

## Rollback / retire

Rollback is already applied: the four unpromoted genre references and stable IDs
were removed from the public skills, and the input-only fixtures were moved under
`maintainers/evals/fixtures/`. To retire a claim, delete its staged fixture and add
a dated row here explaining the counterevidence; do not silently re-add its public
ID. To retry, create a target-only candidate package against the recorded baseline,
hash prompt/input/output bytes, use new executor contexts and a new independent
reviewer, then append—not overwrite—the new decision.

## Production-form transfer decision

The shared production-form reference passed a separate target-only, two-executor
blind transfer over unrelated ink-dynamic-comic and stylized-3D educational scenes.
The candidate arm won at confidence `0.82`; the independent reviewer recommended
promotion with narrow wording corrections and no second comparison. Unlike the
genre runs above, the repository retains the fixture, anonymous arms, executor and
reviewer briefs, verdict, evaluated/promoted reference bytes, package hashes, mapping,
outcome-evidence boundary, and rollback instructions in
`production-form-2026-07/decision.md`.

This decision claims improved text-level production-form translation only.
`media_observed: false`; no prompt presence, task completion, resubmission, or
pipeline status is treated as evidence of rendered-media quality.
