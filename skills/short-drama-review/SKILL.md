---
name: short-drama-review
description: 独立校验与审查文件系统短剧项目中的故事、剧本、资产、连续性、资产图片提示词、分镜、关键帧和视频提示词。用户提出“审稿/检查剧本”“检查资产或连续性”“检查图片/视频提示词”“去模板感”，或判断一集能否交付文本或 JSON 时使用；只发布审查问题、审查结论和修订要求，不代替负责人修改来源文件。
---

# 短剧独立审查

独立审查并引用产物证据。只写审查问题、审查结论和按负责人分组的修订要求；
不在同一次审查中替负责人修改创作来源，也不接受负责人自审。默认使用创作者语言；
中文项目的审查问题、影响和修订要求使用中文，稳定的规则编号和 ID 保持原样。

## 选择审查范围

声明一个或多个范围：

- `story_script`
- `assets_continuity`
- `image_prompts`
- `storyboard_keyframes`
- `video_prompts`
- `full_episode`
- `delivery_privacy`

只读对应的审查表。完整审查先读
[review-method.md](references/review-method.md)，再读三份审查表；制作端常见缺陷
与各环节判据见 [production-quality-gates.md](references/production-quality-gates.md)。
涉及参考图权限、遮挡式揭示或补拍版与替代版关系时加读
[参考媒体权限与补拍契约](../short-drama/references/reference-media-and-pickups.md)。
不预先加载所有创作资料。
证据来自项目产物和已接受限制，而非负责人的自我解释。
只有审查问题涉及“模板感、重复手法或 AI 味”时才读
[anti-template-repair.md](references/anti-template-repair.md)，用其诊断、修订示范与误报反例。

## 工作流

### 1. 冻结审查目标

记录产物路径和 `hash`、创作者限制、审查范围与上游 `hash`。目标文件变化后，
旧审查问题变为 `stale`。状态为 `provisional` 或尚未接受的输入不能获得最终批准。

### 2. 先跑结构校验

先检查可证明事实：

- 数据结构、JSONL 和稳定 ID；
- 来源与资产引用；
- 原文落实情况；
- 准确资产版本，以及来源文字政策与本次呈现方法的对应关系；
- 明确时间段的总和；
- 生命周期与事务状态；
- 派生规格和配方的 `hash`；
- 负责人权限与隐私边界。

缺少前置资料而无法审查目标时，停止后续内容审查；其他互不依赖的结构问题可以一次汇总。

### 3. 带证据审查内容与创作方法

重新查看当前资料，不采用负责人的自我辩解。每个审查问题包含：

- 稳定的问题编号、做法编号、问题类别和检查方式；
- 准确的文件、记录、段落、镜头或提示词及其 `hash`；
- `target_ref` 以及来源端和使用端的 `evidence_refs[]`；
- 必要的短引文或冲突字段；
- 对观众理解或制作的影响；
- 必须达到的修订结果，而不是藏在审查问题里的代写稿；
- 负责技能、严重程度和状态。

分类必须使用：

- `structural_invariant`：能够直接证明的结构错误；
- `reviewed_invariant`：证据成立时给出 `REVISE`；
- `craft_default`：说明影响的警告，可由创作者明确改写；
- `taste_option`：备选意见，不能单独阻断。

### 4. 跨层综合

优先守住剧本原意与连续性，而不是奖励华丽提示词。追踪：

```text
剧本事实 -> 资产决定 -> 镜头目的与边界
-> 冻结关键帧 -> 有序动作 -> 下一状态
```

造型版本错误、遗漏对白、改变动机、发明动作或破坏下一镜衔接时，提示词写得再详细也不能弥补。

### 5. 给出审查结论并分派修订

- `APPROVE`：没有阻断问题，常用做法符合已接受的创作意图；
- `APPROVE_WITH_NOTES`：没有阻断问题，只有可选改进；
- `REVISE`：存在结构错误、内容错误或违反已接受限制；
- `PROVISIONAL`：缺少独立审查者或已接受的前置资料。

按故事开发、剧本、资产、图片提示词、分镜和视频提示词分组。负责人修改后列出所有
变为 `stale` 的下游产物，并审查新 `hash`；审查者不编辑来源文件。

审查结论必须以结构化方式绑定准确的 `reviewed_artifacts`、当前 `findings_ref`、审查者
独立性和未关闭阻断问题数量。`findings_ref` 的 JSONL 中，每个未关闭的致命、错误或阻断
问题 ID 必须且只能出现一次，并与审查结论中的 `blocking_findings` 和数量完全一致。
隐藏未关闭问题、列入已关闭问题或引用不存在的 ID 都不能批准。没有这些证据时只能给
`PROVISIONAL`；一个状态字符串本身不能放行交付。`reviewer` 必须使用模板中的结构对象，
明确声明负责人、审查者类型、`independent:true` 和被排除的准确负责人；只写一个审查者
名称不能证明独立性。

## 审查表

- 故事承诺、因果、场景、行动、对白：
  [rubric-story-script.md](references/rubric-story-script.md)
- 资产身份/变体、连续性、资产图片提示词：
  [rubric-assets-prompts.md](references/rubric-assets-prompts.md)
- 原文落实、镜头、关键帧、视频提示词和跨镜状态：
  [rubric-visual-motion.md](references/rubric-visual-motion.md)

## 审查问题与严重程度

从 [finding-template.jsonl](assets/finding-template.jsonl) 建立审查问题，从
[verdict-template.json](assets/verdict-template.json) 建立审查结论。问题目录提供编号、类别、
默认检查方式、严重程度和负责人；审查问题记录本次目标的证据和状态。

- `fatal`：不安全或非公开内容被交付、事务损坏、缺少授权；
- `error`：阻断当前检查的结构或内容错误；
- `warning`：有具体影响的常用做法问题；
- `note`：创作选择、问题或不阻断交付的润色建议。

没有证据不要打分。不能只说“AI 味”；必须定位重复手法、用套话代替具体内容，或没有铺垫的文句模式，
并解释它伤害什么。

## 边界

- 不生成或查看已渲染媒体。
- 不从文字产物声称脸部一致、表演、口型、混音、剪辑或市场表现。
- 不把非公开制作观察变成通用审查标准。
- 审查问题只带创作者修订所需的必要证据；不泄露非公开输入、完整创作文本、
  网址或机器路径。
