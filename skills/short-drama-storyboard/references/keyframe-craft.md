# Frozen Keyframe Craft

## Boundary and instant tests

- `SHT-05` — Project exactly one accepted shot boundary and bind the exact
  Character/Look, Location/View, and Prop/State variants visible there.
- `SHT-06` — Describe one freezeable instant. Ordered action, expression arcs,
  camera movement, and transforming weather belong to motion, not the keyframe.

## Purpose

Describe one frame that can exist at a single instant and accurately anchors the
accepted shot. A keyframe is not a compressed video prompt.

## Ordered recipe

1. **Purpose:** what the audience must notice now.
2. **Focal subject:** exact asset and variant IDs.
3. **Frame:** shot size, angle, lens intent, aspect-aware composition.
4. **Geography:** Location/View, fixed anchors, foreground/background zones.
5. **Boundary projection:** exact start position, pose, gaze, hands, held props.
6. **Performance instant:** one visible expression/tension state, not an arc.
   Pick a channel the current shot size can actually read — gaze, breath, body
   set, object handling, or a held decision. A wide shot cannot carry an eyelid;
   a close-up cannot carry a full-body retreat. Naming only the emotion ("愤怒")
   leaves the translation to a downstream stage, and the keyframe is the first
   frame — a mistranslation there is wrong from frame one.
7. **Light and atmosphere:** inherit accepted direction/time/weather; add only
   frame-relevant detail.
8. **Text policy:** readable/symbolic/blank/postproduction for visible surfaces.
9. **Exclusions:** contradictions or drift likely for this frame.

Identity and boundary facts remain source references. The keyframe owns focal,
composition, camera/lens, frame-only staging, and exclusions.

`text_treatment_refs` must resolve to the asset owner's accepted text-policy
field (or explicitly candidate policy in a provisional chain). A frozen frame
may determine whether the surface is legible in this composition; it may not
replace the source wording or policy with an untraceable prose instruction.

## Start-only drafting discipline

**`SHT-10 · reviewed_invariant`**: rendered keyframe prose may contain only
start-boundary facts; anything first created by shot motion/end is drift.

Keyframe 默认是 shot start，不是“本镜最有戏的时刻”。为避免把 end 提前：

1. 先冻结 `start_boundary_ref`，草拟 prompt 时暂不读 end/motion prose；
2. 只填 start 已成立的 position/pose/gaze/hands/held props/visible state；
3. 再与 end 做“新出现事实”差集；差集中的事实不得出现在 keyframe prompt；
4. 渲染 Markdown 后从自然语言反向提取手位/持物/目光/可见状态，与
   structured boundary 再比一次；不能只验 JSON 投影而忽略真正交付的 prompt。

反例：start 是“右手空置、看对方”，end 是“右手握铃绳、看门”。冻结帧写
“手已握铃绳”即使很好看，也属于 boundary drift。

## Static test

Ask: could a still photographer capture every described fact at once?

Move these to motion:

- ordered verbs (先、再、随后、最终);
- expression changing from A to B;
- camera push/pan/track over time;
- entering/leaving/turning/reaching sequences;
- dialogue delivery arc or sound progression;
- light/weather transforming during the shot.

A single held pose may imply tension, but it must not require several moments.

## Prompt economy

Do not restate full character or location bibles. Bind accepted variants and
repeat only facts the frame needs to prevent ambiguity: distinguishing anchor,
current Look, crucial spatial anchor, held prop, light direction, text state.

Generic “cinematic, 8K, masterpiece” language cannot replace subject identity,
geography, composition, or continuity.

## Failure examples

- incompatible Looks appear in the same frame;
- “turns, runs, then looks back” appears in a still;
- the start hand/prop differs from the shot boundary;
- background changes location identity or orientation;
- light direction resets without source change;
- readable evidence is paired with no-text;
- prompt lists subjects but not their spatial relationship;
- framing has no focal hierarchy.
- structured projection matches start but rendered prompt describes a fact that
  first appears in the shot end or motion.
