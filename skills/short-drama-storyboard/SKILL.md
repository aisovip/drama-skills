---
name: short-drama-storyboard
description: 把已接受的中文短剧剧本和资产转成来源 coverage、有戏剧动机的镜头、连续性边界与冻结关键帧提示词。用户提出“拆分镜/设计镜头/做镜头表”“写首帧/关键帧提示词”“检查轴线、站位、视线、持物连续性”，或需要在不生成媒体的前提下把剧本意义翻译成视觉 coverage 时使用。
---

# 短剧分镜与冻结关键帧

先守住故事意义，再建立 coverage、空间和镜头，最后写冻结关键帧。不在这里写随时间变化的
motion prompt，也不改写剧本或资产真相。默认以创作者语言交付；中文项目使用中文镜头目的、
边界说明和可复制提示词，ID/字段名保持契约形式。

## 渐进加载

始终读取：

- accepted `screenplay.md` 与 `screenplay-index.jsonl`；
- accepted assets/variants 与相关连续性；
- `short-drama.json#/creator_authority/visual_direction` 的 accepted visual direction；
  `unset` 时向创作者呈现选择，不从对话记忆补造。

设计 coverage、blocking、camera、cut 时读
[shot-craft.md](references/shot-craft.md)；只有写冻结帧时读
[keyframe-craft.md](references/keyframe-craft.md)。需要生产端时长基准、景别/运镜
词表或时间片写法时读 [production-shot-grammar.md](references/production-shot-grammar.md)。
所有权或 stale 不清楚时才读 core contract。

- 竖屏多人、单房对白、证据揭示、群体轴线或门内/外 View：
  [blocking-playbooks.md](references/blocking-playbooks.md)
- 需要查看 screenplay → coverage → shot → keyframe 的完整合成正例：
  [screenplay-to-keyframe-example.md](references/screenplay-to-keyframe-example.md)

## 工作流

### 1. 先做 coverage

从 [coverage-template.json](assets/coverage-template.json) 开始，accepted 后发布为
`episodes/<EP>/storyboard/coverage.json`。每个 production-relevant screenplay block
必须有一个 disposition：

- `covered`：被一个或多个 shot 承担；
- `intentional_repeat`：带戏剧/剪辑理由的重复；
- `omitted_with_reason`；
- `nonvisual_context`。

对白、动作、画面文字、VO/OS 或关键 SFX 还在无声遗漏时，不要先设计漂亮镜头。
Coverage 发布时，`shot_refs` 必须逐条指向精确的 shots artifact、已发布 hash 与
`record_id`；裸 `shot_id` 只可用于同一 shots 文件内部关系，不能证明 coverage 所审的
是哪一版镜头。

### 2. 先写镜头目的

使用 [shot-template.jsonl](assets/shot-template.jsonl)，accepted 后发布为
`episodes/<EP>/storyboard/shots.jsonl`。每个 shot 用一句话回答：

- 观众此刻必须注意/感到什么；
- 信息、情绪、alignment 或权力发生什么变化；
- 为什么要新切一镜，而不是留在前一镜。

之后才选择景别和摄影机行为。镜头不是加了镜头形容词的动作段落。

### 3. 绑定空间和资产

绑定精确 Location/View、Character/Look、Prop/State 与 source blocks，并建立：

- 位置、朝向、视线、screen direction 与 axis；
- 进出路线和 fixed location anchors；
- 双手/持物、伤势/服装、文字状态、光向；
- 权威 start/end boundary。

可见字样的呈现必须通过 `text_treatment_refs` 指向 assets owner 已接受的文字政策；
预览只能指向带 `authority: candidate` 的候选政策。Shot/Keyframe 可决定构图如何让
文字可见，但不得把 `exact_readable` 偷换成装饰字、凭空写新文案，或用自由字符串
代替 policy ref。

需要的资产/状态缺失或含混时，向 assets/write 发 revision；不猜 binding。
在 creator 要求的 end-to-end preview 中，只能对唯一、非 unresolved proposal
建 provisional coverage/shot/keyframe；候选 ArtifactRef 加 `authority:candidate`，不得
写 accepted binding 或获得最终 approval。

### 4. 设计可实现的编辑镜头

短镜头以一个 primary action 加上读懂后果所需的 reaction 为默认，不是 shot-count 公式。
当单镜无法守住地理、表演、对白或信息变化时拆；新 cut 不增加注意或戏剧价值时合。

Duration 是编辑意图。只有显式计时算术可机械阻断；一般可行性必须带本镜证据审查。

### 5. 默认每镜一个冻结关键帧

使用 [keyframe-template.jsonl](assets/keyframe-template.jsonl) 写结构化 source，发布为
`episodes/<EP>/storyboard/keyframes.jsonl`；再用
[keyframe-prompts.md](assets/keyframe-prompts.md) 渲染可复制缓存。结构化 keyframe
拥有 frame-only 选择；Markdown 不成为第二真相。

把 accepted shot start boundary 与 exact asset variants 投影成一个同时可存在的瞬间：
焦点、构图、camera/lens、空间锚点、姿态、目光、双手/持物、表情、光线、排除项。

关键帧不得包含“先/再/最后”、表演弧、运镜过程或变化中的环境；时间变化交给
`$short-drama-video-prompts`。

### 6. 校验并呈现

先运行 coverage/reference/continuity 结构检查，再按 craft references 自检。按顺序呈现：

1. coverage 缺口与 unresolved；
2. 按场分组的 shot table；
3. 可复制 keyframe prompts；
4. 相对 screenplay 的语义差异；
5. 需要创作者接受的选择。

Storyboard 不能自批；终审交给 `$short-drama-review`。

## 修订

若 motion 需要改 start/end boundary，owner 仍是本 Skill。对照 screenplay meaning
审查提议，修改 shot，展示 stale closure，并刷新 keyframe/motion/review。Motion 文件
不得静默成为第二套 boundary truth。

## 边界

- 不生成图片或视频。
- shot 绑定资产，不把完整外观 prose 复制到每镜。
- 外部执行单位不等于 authored shot identity。
- shot count、每 cut 秒数、lens 分布都不是通用定律。
- 新增/删除 story fact 必须先走 write-owned revision。

## 所有产物

- `episodes/<EP>/storyboard/coverage.json`
- `episodes/<EP>/storyboard/shots.jsonl`
- `episodes/<EP>/storyboard/keyframes.jsonl`
- `episodes/<EP>/storyboard/keyframe-prompts.md`（仅派生缓存）
