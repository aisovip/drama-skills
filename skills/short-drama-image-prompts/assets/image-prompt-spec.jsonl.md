# `image-prompt-specs.jsonl` 填写模板

每行一个对象；本模板明确表示 candidate preview，示例值不是默认答案。删除不适用字段，不要添加媒体任务、供应商或 API 字段。所有上游 refs 都带 `authority:candidate`；创作者接受后由事务发布刷新为 accepted snapshot refs，不能只删状态字样冒充 promotion。

```json
{"spec_id":"IMG-<stable-id>","status":"candidate","purpose":"character_sheet | location_plate | prop_plate | look_state_variant | edit_delta","asset_binding":{"identity_ref":{"owner":"short-drama-assets","artifact":"bible/<identity-owner-file>.jsonl","hash":"<sha256>","record_id":"CHAR/LOC/PROP-<id>","authority":"candidate"},"variant_ref":{"owner":"short-drama-assets","artifact":"bible/<variant-owner-file>.jsonl","hash":"<sha256>","record_id":"LOOK/VIEW/PSTATE-<id>","authority":"candidate"}},"source_refs":[{"artifact":"bible/<owner-file>.jsonl","hash":"<sha256>","field":"/<field>","role":"identity_anchor | variant_delta | geography | scale | text_policy","owner":"short-drama-assets","record_id":"<record>","authority":"candidate"}],"recipe":{"name":"<type-recipe>","version":"<suite recipe version>","hash":"<sha256>"},"intent":{"reuse_job":"<这张参考图后续保持什么>","audience":"<使用者/阶段>"},"identity_or_form_anchors":["<稳定、可见、可比较的锚点>"],"variant_deltas":[{"field":"<变化对象>","observable_change":"<位置/范围/结果>","valid_range":"<接受的有效范围>"}],"composition":{"view":"<观察方向/视图>","framing":"<主体占比或板式>","orientation":"<方向定义>","scale_relation":"<尺度参照>","spatial_relations":["<锚点之间的关系>"]},"appearance":{"materials":["<识别所需材质>"],"palette":"<主次色关系>","lighting":"<光源、方向、用途>","atmosphere":"<有事实依据的气氛>"},"background":{"policy":"clean | contextual | empty_stage","details":"<背景与允许出现内容>"},"text_handling":{"source_policy_ref":{"artifact":"bible/props.jsonl","hash":"<sha256>","field":"/text_policy","owner":"short-drama-assets","record_id":"PROP-<id>","authority":"candidate"},"source_mode":"exact_readable | graphic_only | no_readable_text | pending_creator_text","render_treatment":{"mode":"readable | symbolic | blank | postproduction","surface":"<承载面>","exact_text":"<仅 readable 且来自接受源时填写>","layout_or_reserved_area":"<方向/区域/行数>"},"mapping_rationale":"<为何本次呈现保持 source policy>"},"constraints":["<必须出现/保持>"],"negative_constraints":["<仅当前高风险且不矛盾的排除>"],"edit":{"changes":["<有边界变化>"],"preserve":["<身份/构图/光线/未影响区域>"],"continuity_impact":"<影响的 accepted variant/binding 或 none>","target_ref":{"owner":"short-drama-image-prompts","artifact":"<精确目标>","hash":"<sha256>","record_id":"IMG-<target-id>","field":"/generic_prompt","authority":"candidate"},"entity_or_region":"<区域>"},"creator_overrides":[{"rule_id":"<IMG-*>","choice":"<覆盖选择>","rationale":"<原因>"}],"generic_prompt":"<从本规格渲染的可复制通用提示词>","derivation":{"input_hashes":["<sha256>"],"renderer":"generic-markdown","rendered_hash":"<sha256>"},"provenance":"creator_project"}
```

## 类型取舍

- `character_sheet`：`identity_or_form_anchors`、一个 Look、身份友好构图；删掉不适用的 `edit`。没有已接受文字政策且不存在文字承载面时，也删除整个 `text_handling`，不能保留悬空 ref。
- `location_plate`：将 geography 放入 anchors/spatial relations，明确 `empty_stage`；通常无需 `exact_text`。如果画面需要标牌等文字，先由 assets 在对应身份/variant 建立并接受 `text_policy`，再把 ref 指向那个真实字段。
- `prop_plate`：在 anchors 中填写轮廓/功能，在 composition 中填写尺度，在 text policy 做单选。
- `look_state_variant`：必须有 base source ref、清楚 deltas 与 validity；不要把 pose 自动做成 variant。
- `edit_delta`：保留 target/changes/preserve/impact，且所有 source-owned 变化先取得 owner 接受。

候选对象与 accepted 对象分开保存/提交。自然语言修改先生成候选和语义 diff，不直接覆盖本行。
