# `motion-specs.jsonl` 填写模板

每行一个候选运动规格对象。`boundary_refs` 只读并保留 `authority:candidate`；创作者接受后，
通过事务发布刷新为准确的已确认 `hash`。不要加入 `duration_override`、`end_override` 或
`next_shot_write`。以下字符串只说明怎样填写，不是固定答案。

```json
{
  "motion_id": "MOTION-<stable-id>",
  "status": "candidate",
  "shot_ref": {
    "artifact": "episodes/<EP>/storyboard/shots.jsonl",
    "hash": "<sha256>",
    "record_id": "SHOT-<id>",
    "owner": "short-drama-storyboard",
    "authority": "candidate"
  },
  "keyframe_ref": {
    "artifact": "episodes/<EP>/storyboard/keyframes.jsonl",
    "hash": "<sha256>",
    "record_id": "KEY-<id>",
    "owner": "short-drama-storyboard",
    "authority": "candidate"
  },
  "purpose_ref": {
    "artifact": "episodes/<EP>/storyboard/shots.jsonl",
    "hash": "<sha256>",
    "record_id": "SHOT-<id>",
    "field": "/purpose",
    "owner": "short-drama-storyboard",
    "authority": "candidate"
  },
  "coverage_scope": {
    "mode": "master",
    "source_obligations": [
      {
        "kind": "action",
        "source_ref": {
          "owner": "short-drama-write",
          "artifact": "episodes/<EP>/screenplay-index.jsonl",
          "hash": "<sha256>",
          "record_id": "BLK-<id>",
          "authority": "candidate"
        },
        "disposition": "covered_now",
        "motion_field": "/ordered_subject_motion/0"
      },
      {
        "kind": "reaction",
        "source_ref": {
          "owner": "short-drama-storyboard",
          "artifact": "episodes/<EP>/storyboard/shots.jsonl",
          "hash": "<sha256>",
          "record_id": "SHOT-<id>",
          "field": "/purpose",
          "authority": "candidate"
        },
        "disposition": "covered_now | retained_in_master | separate_pickup | requires_storyboard_revision",
        "motion_field": "/<current motion field or none>"
      },
      {
        "kind": "dialogue",
        "source_ref": {
          "owner": "short-drama-write",
          "artifact": "episodes/<EP>/screenplay-index.jsonl",
          "hash": "<sha256>",
          "record_id": "DIALOGUE-<id>",
          "authority": "candidate"
        },
        "disposition": "covered_now | retained_in_master | separate_pickup | requires_storyboard_revision",
        "motion_field": "/audio/0"
      },
      {
        "kind": "reveal",
        "source_ref": {
          "owner": "short-drama-storyboard",
          "artifact": "episodes/<EP>/storyboard/shots.jsonl",
          "hash": "<sha256>",
          "record_id": "SHOT-<id>",
          "field": "/audience_visibility/0",
          "authority": "candidate"
        },
        "disposition": "covered_now | retained_in_master | separate_pickup | requires_storyboard_revision",
        "motion_field": "/performance_arc"
      },
      {
        "kind": "directive",
        "source_ref": {
          "owner": "short-drama",
          "artifact": "project-profile.json",
          "hash": "<sha256>",
          "record_id": "PROJECT-PROFILE",
          "field": "/directives/0",
          "authority": "candidate"
        },
        "disposition": "covered_now | retained_in_master | separate_pickup | requires_storyboard_revision",
        "motion_field": "/<field that carries this project requirement>"
      },
      {
        "kind": "end_boundary",
        "source_ref": {
          "owner": "short-drama-storyboard",
          "artifact": "episodes/<EP>/storyboard/shots.jsonl",
          "hash": "<sha256>",
          "record_id": "SHOT-<id>",
          "field": "/end_boundary",
          "authority": "candidate"
        },
        "disposition": "covered_now | retained_in_master | separate_pickup | requires_storyboard_revision",
        "motion_field": "/end_report"
      }
    ],
    "replacement_intent": "does_not_replace_master | requests_supersession",
    "master_motion_id": null,
    "supplements_motion_ids": []
  },
  "boundary_refs": {
    "duration": {
      "artifact": "episodes/<EP>/storyboard/shots.jsonl",
      "hash": "<sha256>",
      "record_id": "SHOT-<id>",
      "field": "/duration_seconds",
      "value_seconds": 0.0,
      "owner": "short-drama-storyboard",
      "authority": "candidate"
    },
    "start": {
      "artifact": "episodes/<EP>/storyboard/shots.jsonl",
      "hash": "<sha256>",
      "record_id": "SHOT-<id>",
      "field": "/start_boundary",
      "owner": "short-drama-storyboard",
      "authority": "candidate"
    },
    "end": {
      "artifact": "episodes/<EP>/storyboard/shots.jsonl",
      "hash": "<sha256>",
      "record_id": "SHOT-<id>",
      "field": "/end_boundary",
      "owner": "short-drama-storyboard",
      "authority": "candidate"
    },
    "next_start": {
      "artifact": "episodes/<EP>/storyboard/shots.jsonl",
      "hash": "<sha256>",
      "record_id": "SHOT-<next-id>",
      "field": "/start_boundary",
      "access": "comparison_only",
      "owner": "short-drama-storyboard",
      "authority": "candidate"
    }
  },
  "reference_bindings": [
    {
      "artifact_ref": {
        "owner": "short-drama-storyboard",
        "artifact": "episodes/<EP>/storyboard/keyframes.jsonl",
        "hash": "<sha256>",
        "record_id": "KEY-<id>",
        "authority": "candidate"
      },
      "role": "start_frame",
      "may_control": [
        "<本镜 accepted 起始构图与可见状态>"
      ],
      "must_not_control": [
        "<尚未发生的动作/终态/无权威文字>"
      ],
      "admission_status": "unverified | creator_described | visually_inspected",
      "reference_observation_ref": null,
      "unresolved_risks": [
        "<没有观察证据时保留的文字/水印/裁切风险>"
      ]
    }
  ],
  "start_anchor": {
    "pose_balance": "<仅运动必需>",
    "gaze": "<目标>",
    "hands": {
      "left": "<状态>",
      "right": "<状态>"
    },
    "held_props": [
      "<exact binding + hand>"
    ],
    "spatial_relations": [
      "<与行动对象的关系>"
    ]
  },
  "ordered_subject_motion": [
    {
      "order": 1,
      "actor": "<asset binding>",
      "trigger": "<accepted cue>",
      "action": "<可见动作>",
      "direction_or_path": "<方向/路径>",
      "object_or_contact": "<对象/接触>",
      "result": "<阶段结果>",
      "timing": {
        "mode": "relative | explicit",
        "value": "<顺序词或秒区间>"
      }
    }
  ],
  "performance_arc": {
    "trigger": "<source cue>",
    "receive": "<注意变化>",
    "process_visible": "<可见处理>",
    "choice": "<行动/抑制>",
    "landing": "<与 accepted end 相容>"
  },
  "camera": {
    "behavior": "locked | move | transition",
    "motivation": "reveal | pressure | alignment | relationship | transition | deliberate_stillness",
    "intervals": [
      {
        "range": "<相对阶段或秒区间>",
        "mode": "<lock/pan/tilt/dolly/handheld/follow>",
        "path_tempo": "<方向/节奏>",
        "endpoint": "<在 accepted framing/boundary 内>"
      }
    ]
  },
  "environment_motion": [
    {
      "element": "<已有环境元素>",
      "motion": "<有剧情意义的变化>",
      "cause": "<连续性/主体动作>"
    }
  ],
  "audio": [
    {
      "source_ref": {
        "artifact": "<screenplay/shot>",
        "hash": "<sha256>",
        "owner": "short-drama-write",
        "record_id": "<dialogue|VO|OS|SFX-id>",
        "authority": "candidate"
      },
      "kind": "dialogue | VO | OS | SFX | ambience | music",
      "exact_text": "<仅 source 有文本时逐字引用>",
      "delivery_or_spatial_intent": "<不改文本的表演/声源/层级>",
      "timing": "<相对阶段或秒区间>"
    }
  ],
  "timing_plan": {
    "mode": "relative | explicit",
    "phases": [
      "<阶段、overlap 与 landing 空间>"
    ],
    "declared_total_or_endpoint_seconds": 0.0
  },
  "end_report": {
    "projection": {
      "pose": "<reported>",
      "position": "<reported>",
      "gaze": "<reported>",
      "hands": "<reported>",
      "held_props": "<reported>",
      "visible_state": "<reported>"
    },
    "comparison": "match | mismatch | unrealized",
    "source_end_hash": "<sha256>",
    "differences": []
  },
  "reference_frame_economy": {
    "frame_carries": [
      "appearance",
      "composition",
      "base lighting"
    ],
    "repeated_for_motion_only": [
      "<hand/prop/path 等必要局部>"
    ]
  },
  "creator_overrides": [
    {
      "rule_id": "<VID-*>",
      "choice": "<覆盖>",
      "rationale": "<理由>"
    }
  ],
  "generic_prompt": "<从本规格渲染的可复制通用视频提示词>",
  "derivation": {
    "recipe_version": "<version>",
    "input_hashes": [
      "<sha256>"
    ],
    "rendered_hash": "<sha256>"
  },
  "provenance": "creator_project"
}
```

`reported_end` 不成为下一镜的输入；出现 `mismatch` 时保持来源文件不变，修改运动说明或向分镜技能
提出修改请求。末镜若没有已经存在的下一镜，删除范例的 `next_start`，改用
`next_start_locator` 或已有的单集交接 `ArtifactRef`；不伪造记录或 `hash`。
没有附加参考媒体时 `reference_bindings` 用空数组；每条绑定记录只决定声明的 `role`。
普通完整版本用 `master`；同一 `motion-specs.jsonl` 内的局部补拍或替代版本用
`master_motion_id` 与 `supplements_motion_ids` 指向已有记录。不能给同一文件写自己的
`hash`；下游审查会用文件 `hash` 和记录 ID 绑定快照。`source_obligations` 把动作、反应、
对白、揭示、项目要求与镜头终点分别指向来源，并用 `motion_field` 标出当前实现；
未承担项仍留在母版、另一补拍版或分镜修改中，不能靠一段笼统说明消失。

运动规格只能提出 `replacement_intent: requests_supersession`，不能在自身写入审查引用
或宣布替代。独立审查者在下游审查结论的 `supersession_decisions` 中绑定固定的
候选版和母版的固定 `hash` 后作决定，避免运动规格与审查结论互相引用、`hash` 无法稳定。
没有创作者或参考图权利人的文字观察记录，参考图检查状态保持 `unverified`；本模板不查看
或生成媒体。
通用规格不含供应商、模型、远程任务或接口字段。
