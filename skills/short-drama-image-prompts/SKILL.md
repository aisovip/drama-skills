---
name: short-drama-image-prompts
description: 为已确认的短剧角色、造型、场景、视图、道具和状态编写或修改可复制的通用资产图片提示词。用户提到角色设定图、人物参考图、场景空镜、场景板、道具图、造型或状态变体、局部编辑提示词、资产图片 prompt，或要求用自然语言修改现有图片提示词时直接使用；只产出结构化规格与 Markdown 文本，不生成图片、不调用模型或供应商 API。
---

# 短剧资产图片提示词

把已接受的资产事实编译为“能认出、能复用、能区分状态”的参考图提示词。这里的产品是提示词，不是图片。

## 进入条件与边界

- 可从现成项目直接进入，不要求先做故事开发；先定位 `short-drama.json` 和唯一匹配版本的 sibling core。
- 读取 core 的 `references/contract-and-ownership.md` 与 `references/knowhow-index.md` 中 `IMG-*`、`AST-*`、`CON-*`。
- 输入必须是已接受的 `CHAR/LOOK`、`LOC/VIEW` 或 `PROP/PSTATE` 精确 ID 与快照引用。未决指代、冲突变体或未知状态退回 `$short-drama-assets`，不代猜。
- 若 creator 明确要求全链预览，可对唯一、非 unresolved 的 asset proposal 写
  `candidate` prompt；source refs 加 `authority:candidate`，文档标明 provisional/
  not delivery-ready，不得声称 accepted。
- 本 skill 只拥有构图、提示词专用约束及 edit 的 change/preserve；身份、地理、资产状态仍由 assets 拥有。
- 始终保留 provider-neutral 的通用提示词。不得创建图片、媒体任务、API 请求、模型参数、轮询记录或画质结论。

## 按任务加载资料

| 任务 | 必读资料 |
|---|---|
| 新建任意资产提示词 | [通用配方与视觉锚点](references/common-recipe.md) |
| 人物设定图 | 加读 [人物与造型](references/character-and-look.md) |
| Look、View 或 PState 变体 | 加读 [造型与状态变体](references/look-and-state-variant.md) |
| 场景空镜或 View | 加读 [场景与地理](references/location-plate.md) |
| 道具或 PState | 加读 [道具、尺度与文字](references/prop-plate.md) |
| 局部修改或自然语言改 prompt | 加读 [编辑与修订](references/edit-and-revision.md) |
| 自检、复核、失败诊断 | [审查量表与合成案例](references/review-and-fixtures.md) |

写规格时使用 [结构化规格模板](templates/image-prompt-spec.jsonl.md)，交付文本使用 [Markdown 模板](templates/image-prompts.md)。只加载当前类型所需资料。

## 工作流

### 1. 确认目的而非先堆风格词

先回答：这张参考图以后要帮助谁保持什么一致？选择一种主类型：

- `character_sheet`：识别同一人物的一套已接受 Look；
- `location_plate`：固定一个 Location 的 View、方向和地理；
- `prop_plate`：固定道具的尺度、形制、功能和当前 State；
- `look_state_variant`：在同一身份上突出有因果与有效范围的差异；
- `edit_delta`：对精确目标做有边界的修改，同时声明保留集。

一个规格只承担一个主要复用目的。需要不同 Look/View/State 时分开写，不把互斥状态揉成“大全图”。

### 2. 建立证据卡

从接受快照记录：

1. exact asset + variant ID；
2. stable anchors 与本 variant 的 delta；
3. 来源 artifact/hash/field pointer；
4. 用途、构图、背景、光线与文字政策；
5. 必须出现、必须保持和明确排除的内容；
6. 未决定项以及 creator 的明确覆盖。

只带入当前操作必需的信息。私有引用在文本中仅写 `REF-*`，不泄露本地路径、URL 或原始内容。

### 3. 按重要性编译规格与通用提示词

按“用途/主体 → 识别锚点 → 状态差异 → 构图/方向/尺度/空间关系 → 材质/色彩/光线 → 背景 → 文字政策 → 排除/保留”组织。身份、地理、尺度和可读文字等高信息事实先于“精致、电影感”等泛化审美词。

- `structural_invariant`：绑定精确接受 ID/版本；edit 写清 target/hash/region、changes、preserve、continuity impact；`readable` 不得与全局 no-text 并存。
- `reviewed_invariant`：人物在一个规格中保持同一身份和一套连贯 Look；场景保持可导航地理；道具保持可辨尺度、形制与功能。
- `craft_default`：用少量可观察、彼此正交的锚点；负面约束只防止当前风险，不写长篇万能禁词。
- `taste_option`：写实/绘制、镜头审美、色彩浓度、文风密度由创作者决定。

### 4. 做矛盾与可复用性审查

逐项检查：锚点是否互相打架；临时状态是否污染身份；空间关系是否能画在同一画面；构图是否服务参考用途；文字政策是否可执行；排除项是否误杀必需事实。语义质量用证据复核，不用词数、形容词数或固定提示词长度硬判。

### 5. 让创作者接受，再写正式产物

先展示人能读懂的预览：绑定对象、关键选择、警告与 copyable prompt。接受后写：

- `episodes/<EP>/assets/image-prompt-specs.jsonl`：权威规格；
- `episodes/<EP>/assets/image-prompts.md`：由已接受规格和 recipe hash 重渲染的缓存视图。

跨文件发布遵循 core 的事务与恢复流程；不得以半成品覆盖已接受版本。

## 自然语言修订

用户可直接说“外套保持不变，只把袖口变湿”“场景里不要出现演员”。不要让用户编辑 JSONL。

1. 把请求解析为字段级候选 diff，并标记 source-owned 事实；
2. 展示 `before → after`、影响的绑定/连续性、未映射或有损内容；
3. 等待接受或拒绝；拒绝时原规格与 Markdown 不变；
4. 接受后先提交规格，再从规格重渲染 Markdown。

若 Markdown 被手改：`restore` 先预览恢复；`adopt` 只把可无损映射的改动变成规格提案。无法映射的文句阻断 adopt，绝不让缓存反向静默夺权。详见 [编辑与修订](references/edit-and-revision.md)。

## 完成标准

- 每个规格能追溯到精确接受资产与 variant，且 generic prompt 可独立复制；
- 类型配方完整，重要事实在泛化审美词之前，无未决占位或内部工作指令；
- edit 同时说明改什么、保留什么、连续性影响什么；
- 已运行本地结构检查，再交给独立 `$short-drama-review` 做证据化语义复核；
- 交付中没有媒体、远程执行任务/API、远端 ID、私有映射或“生成成功”声明。
