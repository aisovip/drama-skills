# `image-prompt-specs.jsonl` 填写模板

每行一个候选规格对象，用于接受前预览；示例值不是默认答案。删除不适用字段，不要添加
媒体任务、供应商或接口字段。所有上游引用都带 `authority:candidate`；创作者接受后，
通过事务发布改成指向准确已接受快照的引用。不能只删除状态字样，假装已经接受。

```json
{
  "spec_id": "IMG-<stable-id>",
  "status": "candidate",
  "purpose": "character_sheet | location_plate | prop_plate | look_state_variant | edit_delta",
  "asset_binding": {
    "identity_ref": {
      "owner": "short-drama-assets",
      "artifact": "bible/<identity-owner-file>.jsonl",
      "hash": "<sha256>",
      "record_id": "CHAR/LOC/PROP-<id>",
      "authority": "candidate"
    },
    "variant_ref": {
      "owner": "short-drama-assets",
      "artifact": "bible/<variant-owner-file>.jsonl",
      "hash": "<sha256>",
      "record_id": "LOOK/VIEW/PSTATE-<id>",
      "authority": "candidate"
    }
  },
  "source_refs": [
    {
      "artifact": "bible/<owner-file>.jsonl",
      "hash": "<sha256>",
      "field": "/<field>",
      "role": "identity_anchor | variant_delta | geography | scale | text_policy",
      "owner": "short-drama-assets",
      "record_id": "<record>",
      "authority": "candidate"
    }
  ],
  "reference_bindings": [
    {
      "artifact_ref": {
        "owner": "short-drama-assets",
        "artifact": "bible/<owner-file>.jsonl",
        "hash": "<sha256>",
        "record_id": "<accepted-reference-record>",
        "authority": "candidate"
      },
      "role": "composition",
      "may_control": [
        "<本次允许借用的构图事实>"
      ],
      "must_not_control": [
        "<身份/内容/文字/状态等禁入事实>"
      ],
      "admission_status": "unverified | creator_described | visually_inspected",
      "reference_observation_ref": null,
      "unresolved_risks": [
        "<没有观察证据时保留的文字/水印/裁切风险>"
      ]
    }
  ],
  "recipe": {
    "name": "<type-recipe>",
    "version": "<suite recipe version>",
    "hash": "<sha256>"
  },
  "intent": {
    "reuse_job": "<这张参考图后续保持什么>",
    "audience": "<使用者/阶段>"
  },
  "identity_or_form_anchors": [
    "<稳定、可见、可比较的锚点>"
  ],
  "variant_deltas": [
    {
      "field": "<变化对象>",
      "observable_change": "<位置/范围/结果>",
      "valid_range": "<接受的有效范围>"
    }
  ],
  "composition": {
    "view": "<观察方向/视图>",
    "framing": "<主体占比或板式>",
    "orientation": "<方向定义>",
    "scale_relation": "<尺度参照>",
    "spatial_relations": [
      "<锚点之间的关系>"
    ]
  },
  "appearance": {
    "materials": [
      "<识别所需材质>"
    ],
    "palette": "<主次色关系>",
    "lighting": "<光源、方向、用途>",
    "atmosphere": "<有事实依据的气氛>"
  },
  "background": {
    "policy": "clean | contextual | empty_stage",
    "details": "<背景与允许出现内容>"
  },
  "text_handling": {
    "source_policy_ref": {
      "artifact": "bible/props.jsonl",
      "hash": "<sha256>",
      "field": "/text_policy",
      "owner": "short-drama-assets",
      "record_id": "PROP-<id>",
      "authority": "candidate"
    },
    "source_mode": "exact_readable | graphic_only | no_readable_text | pending_creator_text",
    "render_treatment": {
      "mode": "readable | symbolic | blank | postproduction",
      "surface": "<承载面>",
      "exact_text": "<仅 readable 且来自接受源时填写>",
      "layout_or_reserved_area": "<方向/区域/行数>"
    },
    "mapping_rationale": "<为何本次呈现保持 source policy>"
  },
  "constraints": [
    "<必须出现/保持>"
  ],
  "negative_constraints": [
    "<仅当前高风险且不矛盾的排除>"
  ],
  "edit": {
    "changes": [
      "<有边界变化>"
    ],
    "preserve": [
      "<身份/构图/光线/未影响区域>"
    ],
    "continuity_impact": "<影响的 accepted variant/binding 或 none>",
    "target_ref": {
      "owner": "short-drama-image-prompts",
      "artifact": "<精确目标>",
      "hash": "<sha256>",
      "record_id": "IMG-<target-id>",
      "field": "/generic_prompt",
      "authority": "candidate"
    },
    "entity_or_region": "<区域>"
  },
  "creator_overrides": [
    {
      "rule_id": "<IMG-*>",
      "choice": "<覆盖选择>",
      "rationale": "<原因>"
    }
  ],
  "generic_prompt": "<从本规格渲染的可复制通用提示词>",
  "derivation": {
    "input_hashes": [
      "<sha256>"
    ],
    "renderer": "generic-markdown",
    "rendered_hash": "<sha256>"
  },
  "provenance": "creator_project"
}
```

## 类型取舍

- `character_sheet`：在 `identity_or_form_anchors` 中填写身份识别点，绑定一个造型版本，
  再选择便于识别的构图；删除不适用的 `edit`。没有已接受文字政策且不存在文字承载面时，
  也删除整个 `text_handling`，不能保留悬空引用。
- `location_plate`：把场景地理写入 `identity_or_form_anchors` 和 `spatial_relations`，明确
  `empty_stage`；通常无需 `exact_text`。如果画面需要标牌等文字，先由资产技能在对应
  身份或版本中建立并接受 `text_policy`，再把引用指向真实字段。
- `prop_plate`：在 `identity_or_form_anchors` 中填写轮廓与功能，在 `composition` 中填写
  尺度，并在文字政策中选择一种处理方式。
- `look_state_variant`：必须有基础来源引用、清楚的变化和有效范围；不要把姿势自动做成新版本。
- `edit_delta`：保留目标、`changes`、`preserve` 和影响；由上游负责的变化要先取得其负责人接受。

`reference_bindings` 不是普通参考图清单：每条只声明一个主要用途，并分别写清
可以参考和不能照搬的内容。没有参考媒体时用空数组；不要保留占位引用。构图、尺度或
效果参考不能因为绑定了整张图，就用来决定人物身份、文字或故事状态。只有创作者或参考图
权利人提供的文字说明，或运行环境获授权后对输入参考所作的视觉检查，才能产生准确的
`reference_observation_ref`；否则 `admission_status` 保持 `unverified` 并列出风险。
检查输入参考不等于生成或验收输出媒体。

候选对象与已接受对象分开保存和提交。自然语言修改先生成候选和内容差异，不直接覆盖本行。
