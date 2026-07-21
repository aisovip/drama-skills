# 私有卡片与 Coverage Matrix

## 内容导航

- 卡片共通纪律
- Observation card schema
- Decision card schema
- 完全合成例子
- 题材 × 机制 coverage matrix

## 卡片共通纪律

卡片只保存在维护者指定的隔离工作区。用随机内部 ID、内容 hash 或抽象 locator 追溯证据；
不要在卡片之外复制整段剧本。观察和解释分栏，未知保持未知。一个项目要先通读完整文本链再制卡，
不能把搜索命中当作完整上下文。

`genre_axes` 描述题材、受众承诺和情绪合同；`mechanism_axes` 描述实现机制，不把桥段名当机制。
`evidence` 记录能复核的位置与观察，不记录可识别原文。`counterevidence` 即使为空也必须解释寻找范围。
先按项目、分集、剧本版本与分镜版本还原 `version_chain`，再判断每层记录的 `source_role`：创作来源、
派生投影、修改请求、执行任务或结果证据不能互相冒充。`creator_overrides` 单列，避免把创作者的明确取舍
误读成系统规律。没有直接检查媒体时固定写 `media_observed: false`；提示词存在、任务成功或提交次数只说明
流程活动，不能填进 `outcome_evidence` 冒充效果证明。

## Observation card schema

```yaml
card_type: observation_card
card_id: obs-internal-id
source_project_ref: opaque-project-ref
chain_read:
  available_layers: [brief, story, episode_map, screenplay, assets, continuity, image_prompt_text, storyboard_text, video_prompt_text, review]
  missing_layers: []
  version_chain: [opaque-project-version, opaque-episode-version, opaque-script-version, opaque-board-version]
  creator_overrides: [bounded-override-or-none]
genre_axes:
  surface_genre: abstract-label
  audience_promise: abstract-promise
  emotional_contract: abstract-contract
mechanism_axes: [mechanism-label]
observation:
  setup_state: what-the-audience-can-understand
  pressure_or_question: dramatic-problem
  character_action: playable-action
  information_change: audience-state-change
  turn_or_payoff: observable-dramatic-result
  downstream_translation: how-text-production-layers-preserve-or-alter-intent
evidence:
  direct_observations:
    - locator: opaque-layer-and-record-ref
      source_role: creative_source | derived_projection | revision_request | execution_task | outcome_evidence
      note: paraphrased-observation-without-source-wording
  agent_interpretation: bounded-causal-reading
  unknowns: []
media_observed: false
outcome_evidence:
  available: false
  kind: none | authorized_media_review | audience_or_creator_outcome
  limitations: [text-only-chain-does-not-prove-rendered-result]
counterevidence:
  searched: what-was-checked
  findings: []
  alternate_explanations: []
privacy:
  contains_source_wording: false
  contains_identifiers: false
  public_eligible: false
confidence: tentative | supported | conflicted
```

## Decision card schema

```yaml
card_type: decision_card
decision_id: dec-internal-id
observation_refs: [obs-internal-id]
candidate_claim:
  problem: transferable-dramatic-or-production-problem
  heuristic: conditional-option-not-command
  expected_observable_effect: text-level-effect
classification: bounded_pattern | craft_option | rejected_generalization | conflict_pending
applies_when:
  genre_axes: [abstract-axis]
  audience_state: required-state
  character_state: required-state
  production_constraints: [text-production-constraint]
fails_or_changes_when:
  counterexample_refs: [obs-counterexample-id]
  warning_signals: [signal]
  alternatives: [alternative-mechanism]
conflicts:
  competing_claims: []
  resolution_or_open_question: explanation
sampling_role:
  matrix_cells: [genre-axis-x-mechanism-axis]
  next_contrast_to_read: abstract-sampling-intent
decision:
  status: hold | synthesize | narrow | reject | propose
  rationale: semantic-judgment-not-frequency
review:
  reviewer_ref: null
  reviewed_at: null
  notes: []
```

## 完全合成例子

下例由零构造，只演示抽象层级，不对应任何来源项目：

```yaml
card_type: observation_card
card_id: obs-synthetic-001
source_project_ref: synthetic-only
chain_read:
  available_layers: [brief, story, episode_map, screenplay, assets, continuity, image_prompt_text, storyboard_text, video_prompt_text, review]
  missing_layers: []
  version_chain: [synthetic-project-v1, synthetic-script-v1, synthetic-board-v1]
  creator_overrides: [none]
genre_axes:
  surface_genre: community-workplace-comedy
  audience_promise: overlooked-newcomer-earns-agency
  emotional_contract: embarrassment-turns-into-earned-recognition
mechanism_axes: [public-misreading, delayed-capability-proof]
observation:
  setup_state: the-audience-knows-the-newcomer-notices-a-routing-error
  pressure_or_question: speaking-up-risks-looking-incompetent
  character_action: the-newcomer-quietly-reroutes-one-delivery
  information_change: coworkers-see-the-result-before-the-reason
  turn_or_payoff: ridicule-reverses-only-after-a-specific-consequence
  downstream_translation: shots-preserve-who-knows-what-and-prompts-stage-the-action-before-the-reaction
evidence:
  direct_observations:
    - locator: synthetic-screenplay-scene-03
      source_role: creative_source
      note: action-causes-visible-result-before-explanation
  agent_interpretation: withholding-the-reason-keeps-the-proof-dramatic-rather-than-verbal
  unknowns: [whether-a-warmer-genre-needs-a-softer-public-reaction]
media_observed: false
outcome_evidence:
  available: false
  kind: none
  limitations: [synthetic-text-only-example]
counterevidence:
  searched: synthetic-alternate-scene
  findings: [early-explanation-removes-the-misreading-but-improves-closeness]
  alternate_explanations: [specific-consequence-may-matter-more-than-information-order]
privacy:
  contains_source_wording: false
  contains_identifiers: false
  public_eligible: false
confidence: tentative
```

对应 decision card 应把结论限定为一个可选机制：当观众已理解人物能力、场内人物仍误读、且后果能被表演时，
可先呈现行动后果再解释原因；若题材承诺亲密协作或误读会破坏人物好感，就改用共同发现。不得写成
“逆袭题材必须延迟解释”。

## 题材 × 机制 coverage matrix

矩阵每一格使用以下记录，不用计数替代判断：

```yaml
cell_id: genre-axis-x-mechanism-axis
genre_and_promise: abstract-genre-plus-audience-promise
mechanism: dramatic-or-production-mechanism
supporting_observation_refs: []
opposing_observation_refs: []
boundary_notes: []
conflicts_or_alternatives: []
chain_gaps: []
confidence: empty | tentative | supported | conflicted
next_sample_intent: contrast-or-gap-to-seek
```

选样仪表可以显示各轴是否为空、哪些项目链缺层、哪些卡片互相冲突；它只能触发下一轮定性阅读。
禁止把格内项目数、题材占比、评分均值或高频词直接转换成写作公式、强制阈值或质量排序。
