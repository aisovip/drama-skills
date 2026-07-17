---
name: short-drama-review
description: 独立校验与审查文件系统短剧项目中的故事、剧本、资产、连续性、资产图片提示词、分镜/关键帧和视频提示词。用户提出“审稿/检查剧本”“检查资产或连续性”“检查图片/视频提示词”“去模板感”，或判断一集能否交付文本/JSON 时使用；只发 findings/verdict/revision requests，不代改 owner source。
---

# 短剧独立审查

独立审查并引用 artifact 证据。只写 finding、verdict 与按 owner 分组的 revision request；
不在同一审查 pass 中替 owner 修创作 source，也不接受 owner 自批。默认使用创作者语言；
中文项目的 finding、影响和修订要求使用中文，stable code/ID 保持契约格式。

## 选择 scope

声明一个或多个 scope：

- `story_script`
- `assets_continuity`
- `image_prompts`
- `storyboard_keyframes`
- `video_prompts`
- `full_episode`
- `delivery_privacy`

只读对应 rubric。Full review 先读
[review-method.md](references/review-method.md)，再读三个 rubric；生产端高频缺陷
与各环节判据见 [production-quality-gates.md](references/production-quality-gates.md)。
不预载所有 craft manual。
证据来自项目 artifact 和 accepted constraints，而非 owner 的自我解释。
只有 finding 涉及“模板感/重复机制/AI味”时读
[anti-template-repair.md](references/anti-template-repair.md)，用其诊断、修订示范与误报反例。

## 工作流

### 1. 冻结审查目标

记录 artifact path/hash、creator constraints、scope 与 upstream hashes。目标字节变化后，
旧 finding 变 stale。Provisional 或未接受的输入不能获得最终 approval。

### 2. 先跑结构校验

先检查可证明事实：

- schema/JSONL、stable IDs；
- source/asset references；
- coverage dispositions；
- exact variant 与 source-policy → render-treatment binding；
- explicit timing sums；
- lifecycle/transaction state；
- derived spec/recipe hashes；
- owner permissions 与 privacy boundary。

缺失 prerequisite 让目标不可审时，停止昂贵语义审查；其他独立结构问题可一次汇总。

### 3. 带证据审查语义和 craft

使用新鲜推理，不采用 owner 的辩解。每个 finding 包含：

- stable diagnostic code、know-how rule ID、class、enforcer；
- exact file/record/block/shot/prompt 与 hash；
- `target_ref` 与 source/consumer 两端的 `evidence_refs[]`；
- bounded quote 或冲突字段；
- audience/production impact；
- required outcome（不是藏在 finding 里的代写稿）；
- owner skill、severity、status。

分类必须使用：

- `structural_invariant`：确定性错误；
- `reviewed_invariant`：证据成立时给 `REVISE`；
- `craft_default`：说明影响的 warning，可 override；
- `taste_option`：note/alternative，不能单独阻断。

### 4. 跨层综合

优先守住 source meaning 与 continuity，而不是奖励华丽 prompt。追踪：

```text
screenplay fact -> asset decision -> shot purpose/boundary
-> frozen keyframe -> ordered motion -> next state
```

错误 Look、遗漏 dialogue、改变 motive、发明 action 或打破下一镜时，prompt 越详细也不加分。

### 5. 出 verdict 并路由修订

- `APPROVE`：无 blocker，default 符合 accepted intent；
- `APPROVE_WITH_NOTES`：无 blocker，仅有可选改进；
- `REVISE`：存在结构/语义 invariant 失败或违反 accepted constraint；
- `PROVISIONAL`：缺独立 reviewer 或 accepted prerequisite。

按 develop、write、assets、image-prompts、storyboard、video-prompts 分组。Owner 修改后计算
stale closure，审新 hash；reviewer 不编辑 source。

Verdict 必须结构化绑定 exact `reviewed_artifacts`、当前 `findings_ref`、reviewer
independence 与 open blocker count。`findings_ref` 的 JSONL 中每个 open
fatal/error/blocker ID 必须且只能出现一次，并与 verdict 的 `blocking_findings`/count 完全
一致；隐藏 open finding、列入 closed finding 或不存在 ID 都不能批准。没有这些证据时只能
`PROVISIONAL`；状态字符串本身不能解锁 delivery。`reviewer` 必须是模板所示的结构对象，
明确声明 owner、kind、`independent:true` 与精确 excluded owner；裸 reviewer owner 字符串
不能被补写成 independence proof。

## Rubrics

- 故事承诺、因果、场景、行动、对白：
  [rubric-story-script.md](references/rubric-story-script.md)
- 资产身份/变体、连续性、资产图片提示词：
  [rubric-assets-prompts.md](references/rubric-assets-prompts.md)
- Coverage、shots、keyframes、video prompts、跨镜状态：
  [rubric-visual-motion.md](references/rubric-visual-motion.md)

## Finding 与严重度

从 [finding-template.jsonl](assets/finding-template.jsonl) 建 finding，从
[verdict-template.json](assets/verdict-template.json) 建 verdict。Diagnostic catalog 提供
code、class、default enforcer/severity、owner；finding 提供本次 target evidence/status。

- `fatal`：不安全/非公开交付、损坏事务、缺少 authority；
- `error`：阻断当前 gate 的 structural/reviewed invariant；
- `warning`：有具体可能影响的 craft default；
- `note`：taste option、问题或非阻断润色。

没有证据不要打分。不能只说“AI味”；必须定位重复机制、泛化替代或未挣得的 prose pattern，
并解释它伤害什么。

## 边界

- 不生成或查看已渲染媒体。
- 不从文字 artifact 声称脸部一致、表演、口型、混音、剪辑或市场表现。
- 不把非公开生产观察变成 rubric。
- Findings 只带创作者修订所需的 bounded evidence；不泄露非公开输入、完整创作文本、
  URL 或机器路径。
