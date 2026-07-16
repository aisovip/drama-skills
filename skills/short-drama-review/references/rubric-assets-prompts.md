# Assets And Asset-Image Prompt Rubric

## Occurrence and decision

- Does every extracted occurrence point to a source block/hash?
- Is it production-relevant rather than every noun in the screenplay?
- Is the decision explicit: reuse, new identity, new variant, or unresolved?
- Were pronouns, aliases, groups, memories, portraits, and screen content handled
  without guessing?

## Identity versus variant

### Character / Look

Identity: stable face/body/hair anchors, distinguishing marks, voice/behavioral
identity. Look: wardrobe, makeup, hair arrangement, injury, dirt/wetness, disguise,
age/weathering state, validity range.

Fail when a costume change creates a new person or incompatible Looks mix in one
prompt without story reason.

### Location / View

Identity: architecture, layout, entrances, zones, anchors, materials, navigation.
View: camera-facing orientation/zone, time/weather/light state, visible anchors.

Fail when each camera angle becomes a new unrelated location or geography changes
silently between scene and plate.

### Prop / State

Identity: scale, shape, material, function, moving parts, marks, text policy.
State: owner/hand/location, open/closed, clean/damaged/wet/bloodied, contents,
validity.

Fail when a prop teleports, changes scale/material, or readable evidence is erased.

## Prompt recipe review

All prompt types need purpose, exact binding, identifying facts, current variant,
composition, background, lighting, text policy, constraints, and exclusions. Then
apply type-specific criteria:

- **Character sheet:** one identity and coherent Look; useful reference views;
  neutral enough background/light to recognize anchors; no story action chain.
- **Location plate:** navigable geography, orientation, fixed anchors, material,
  palette, light direction, atmosphere; normally empty of cast.
- **Prop plate:** scale cue, shape, materials, wear, function/moving parts, current
  state, viewing angle, isolation, text policy.
- **Edit delta:** exact target/hash/region, changes, preserve set, expected
  continuity impact; no unrelated regeneration.

## Prompt quality failures

- quality/style boilerplate appears before or instead of identity/geography/scale;
- prompt copies the whole bible rather than the needed variant;
- character description mixes immutable anchors with accidental pose;
- location prose is rich but cannot orient entrances/zones;
- prop has no scale or text state;
- negative constraints contradict the required visible fact;
- edit request says “make better” without target/change/preserve;
- rendered Markdown differs from accepted structured spec;
- private URL, source ID, provider task field, or operator complaint leaks in.

Prompt prose elegance is secondary to recognition, reuse, continuity, and clear
control of the current operation.
