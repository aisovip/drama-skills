# Routing Examples

| Request | Route | Important behavior |
|---|---|---|
| “根据这个点子写第一集” | write, or develop if creator asks for alternatives | do not force series planning |
| “把这份旧剧本的人物场景道具拆出来” | assets via minimal write-owned intake | preserve original bytes; preview normalization |
| “先写所有角色定妆图提示词” | image-prompts | require accepted asset identities/Looks, not storyboard |
| “这段对话拆成镜头” | storyboard | establish coverage and purpose before camera decoration |
| “根据这些关键帧写视频提示词” | video-prompts | read shot boundary; do not rewrite it |
| “人物上一镜拿杯子下一镜没了，检查一下” | review | cite continuity evidence; route fix to owner |
| “继续” | router | resume the requested/most recent owner, not blindly run all stages |

## Ambiguous request

For “帮我把这集做完”, show the current creator-facing state and offer no more
than three meaningful actions. Prefer the action that unblocks the requested
delivery. Avoid asking technical questions about schemas or transactions.

## Direct-entry rule

An artifact can be a valid entry even when upstream optional work is absent:

- existing script -> assets;
- accepted assets -> asset image prompts;
- accepted script + assets -> storyboard;
- accepted shots + keyframes -> video prompts.

Create only missing canonical prerequisites owned by the relevant skill. Never
backfill invented creative briefs or series arcs.
