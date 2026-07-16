# Shot Craft

## Rule classification

- `structural_invariant`: machine-checkable structure such as resolved coverage
  and known bindings; a validator may block malformed artifacts.
- `reviewed_invariant`: meaning that must hold but needs evidence-based human or
  model review, such as preserving a source beat.
- `craft_default`: a strong starting practice that may be departed from for a
  stated dramatic reason.
- `taste_option`: an accepted creator or visual-direction choice, never an
  automatic defect by itself.

## Contents

1. Coverage before beauty
2. Dramatic purpose
3. Blocking and geography
4. Framing and camera motivation
5. Duration and cutting
6. Failure patterns
7. Review questions

## Coverage before beauty

`SHT-01` requires every production-relevant screenplay block to receive an
explicit cover, omit, or intentional-repeat disposition.

Map screenplay blocks before inventing shots. Coverage is an accountability map,
not a one-block-one-shot formula. Several blocks may share a shot when continuous
performance and geography preserve their meaning. One block may need several
shots when a reveal, reaction, evidence detail, or spatial change is essential.

The accepted coverage artifact records canonical `shot_refs`, not bare shot IDs:
owner, exact shots artifact, its published hash, and `record_id` identify the
version actually reviewed. Same-artifact relationships may use `*_ids`; crossing
an artifact boundary always uses `*_refs` so stale coverage can be detected.

Repeated coverage is intentional only when the second view creates a new audience
experience—reaction, contradiction, withheld evidence, recontextualization—not
because the first mapping was forgotten.

### Action realization ledger

**`SHT-08 · reviewed_invariant`**：每个 authoritative source action 只有一个
realization shot；repeat coverage 必须增加 reaction/detail/recontextualization。

Coverage count 只证明 block “有人引用”，不证明动作没被提前、重复或遗漏。
对转手、开门、受伤、揭面、拿出证物等 authoritative action，另记：

| Source action | realization shot | start fact | end fact | 其他 coverage 的作用 |
|---|---|---|---|---|
| 右手从衣内取令 | SHOT-02 | 令牌在衣内 | 右手持令 | SHOT-03 只审验纹样/反应 |

- 只有 realization shot 可以从 before 改成 after；
- 前一镜的 end 不得无 source/action 就提前变成 after；
- 后一镜从 after 开始时，motion 不得再演一次完整动作；
- repeat coverage 写清是 detail、reaction 还是 recontextualization，而不是第二次 realization。

## Dramatic purpose

`SHT-02` requires the shot to preserve its source meaning and name what changes
for the audience or character; attractive coverage without that purpose fails
semantic review.

Use this sequence:

1. Identify the source move: action, line, discovery, refusal, transfer, reveal.
2. Name what changes for the audience or a character.
3. Choose whose experience organizes the shot.
4. Decide what must be visible at the start and end.
5. Only then choose framing, camera, and cut.

Useful purposes include orienting geography, aligning with a character, exposing
evidence, withholding information, transferring power, registering a reaction,
or making consequence unavoidable. “中景展示人物说话” is not enough.

## Blocking and geography

Treat location description as navigable space:

- entrances/exits and fixed anchors;
- foreground/midground/background zones;
- who can see or reach what;
- facing and eyeline relationships;
- working side of the axis and screen direction;
- hand/prop ownership and transfer path.

Blocking expresses tactics. Moving closer can pressure or seek alliance; turning
away can withhold; occupying an exit can control; touching evidence can reveal
knowledge. Avoid arbitrary walking inserted only to create motion.

An axis flip is not inherently wrong. It becomes a problem when unmotivated and
confusing. Declare a neutral bridge, visible cross, deliberate disorientation, or
new spatial setup when crossing.

Readable or deliberately unreadable surface text remains an asset-owned policy.
Shots and keyframes carry canonical `text_treatment_refs` to that exact policy
field. They may choose visibility, scale, angle, and focus, but cannot silently
invent wording or change `exact_readable`, `graphic_only`, `no_readable_text`, or
pending status. Candidate previews reference candidate authority and remain
delivery-blocked.

## Framing and camera motivation

`SHT-04` governs the choice: change framing or camera behavior because attention,
pressure, alignment, reveal, or rhythm changes—not to decorate every beat.

- Wide: geography, isolation, group power, simultaneous consequence.
- Medium: interaction, gesture, two-person tactics, readable blocking.
- Close: decision, evidence, concealed reaction, irreversible realization.
- Detail: a story-bearing object/action whose meaning is established.

Change size/angle because attention or relationship changes. Do not escalate from
wide to extreme close merely because the scene gets louder.

Camera behavior is one coherent choice within an interval:

- locked for observation, tension, ritual, entrapment;
- pan/tilt to reveal or transfer attention;
- push/pull to alter intimacy, pressure, or realization;
- track/follow when movement itself is tactical;
- handheld for embodied instability when the visual direction accepts it.

Do not specify locked and moving simultaneously without an explicit transition.

## Duration and cutting

### Short-shot action budget (`SHT-03`)

As a `craft_default`, start with one primary action plus the reaction needed to
make its consequence readable. Combine or expand only when continuous
performance, geography, duration, and the shot's purpose remain legible; this is
not a fixed beat-count validator.

Duration must leave room for readable action, performance, dialogue, and reaction.
Use explicit dialogue length and timed actions as evidence. Treat broad action
load as a review question, not a universal words-per-second blocker.

Cut on a change: new information, gaze, decision, spatial relation, threat,
evidence, or rhythm. Avoid cuts that only restate the same action from another
angle. Preserve enough reaction time for the audience to register consequence.

## Visual-direction option (`SHT-07`)

Lens vocabulary, tempo, and locked, handheld, or formal staging remain
`taste_option` choices inherited from the accepted visual direction. Review
whether the choice serves this shot; do not enforce one house style.

## Linked boundary (`CON-01`)

The shot's accepted end boundary must match the next shot's accepted start, or
the owning artifact must declare a revision/transition. Never hide a mismatch in
camera prose.

## Failure patterns

- shot list paraphrases screenplay but never states viewing purpose;
- anonymous “人物” replaces exact accepted assets;
- one shot crosses location or time without montage/ellipsis;
- dialogue is present but the reaction/payoff is dropped;
- character/prop teleports across the cut;
- every emotional line becomes an extreme close-up;
- camera movement conflicts or serves no attention change;
- boilerplate lighting replaces actual spatial anchors;
- provider batching is mistaken for editorial shot identity.

## Review questions

- What source blocks does this shot cover, omit, or repeat?
- What changes by the end of the shot?
- Why this frame size and camera behavior?
- Can every subject plausibly occupy and move through this geography?
- Are exact Looks, Views, Prop States, hands, and text policy bound?
- Does the end boundary give the next shot a clear start?
- Would removing or combining this shot lose story meaning?
