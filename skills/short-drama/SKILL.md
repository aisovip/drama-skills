---
name: short-drama
description: 基于文件系统初始化、继续、恢复和交付短剧项目，并把具体工作路由给对应短剧 Skill。用户提出“创建/继续短剧项目”“看进度/下一步”“恢复中断或不完整发布”“定点修订/交付”，或直接要求写短剧、拆资产、写资产图片提示词、拆分镜、写视频提示词、审查短剧时使用。
---

# 短剧创作路由

这是轻量项目路由，不在本 Skill 内代写故事、资产提示词、镜头、视频提示词或终审结论。
默认使用创作者的语言；中文项目使用简洁中文呈现状态、差异、选择和下一步。

## 每次请求的起点

1. 使用用户明确路径，或从当前目录向上寻找最近的 `short-drama.json`。
2. 从本 Skill 安装目录解析 sibling suite，读取 `suite-manifest.json`；缺 Skill 或版本混用时先停止变更。
3. 只读 `short-drama.json` 与 `.short-drama/state.json` 摘要；不要一次加载全部创作文件。
4. 在 status 或写入前先运行事务恢复。发现外部编辑冲突时保留原字节，提供 adopt、restore、merge，不静默覆盖。
5. 按创作者当前任务路由；不强制补走整条流水线。

入口、检查点、修订和交付见 [creator-workflow.md](references/creator-workflow.md)。
所有权、stale、隐私或恢复有疑问时读
[contract-and-ownership.md](references/contract-and-ownership.md)。
意图含混时读 [routing-examples.md](references/routing-examples.md)。
只在需要把 rule ID 定位到 craft owner 时读
[knowhow-index.md](references/knowhow-index.md)；router 不代替 craft skill 判断。

## 意图路由

| 创作者意图 | 路由 |
|---|---|
| 开发点子、故事承诺、系列、分集地图 | `$short-drama-develop` |
| 写/改单集契约、因果节拍、剧本 | `$short-drama-write` |
| 拆人物/造型、地点/视图、道具/状态 | `$short-drama-assets` |
| 写人物/地点/道具/edit 图片提示词 | `$short-drama-image-prompts` |
| 做 coverage、镜头或冻结关键帧 | `$short-drama-storyboard` |
| 写动作/表演/运镜/声音视频提示词 | `$short-drama-video-prompts` |
| 校验、审查或发修订请求 | `$short-drama-review` |

创作者明确意图优先于名义上的“下一检查点”。C2 资产接受后，图片提示词和 storyboard
是平行分支；创作者只要其中一支时，不强迫等待另一支。

## 初始化

没有项目且用户要初始化时：

1. 仅确认或合理推断可逆格式默认值：标题、语言、画幅、路径；集数/时长未知就留空。
2. 复制项目模板，不覆盖已有创作者文件。
3. 建立空阶段目录和非公开输入边界。
4. 在 `short-drama.json#/creator_authority` 建立空的 creator constraints、visual
   direction 与 production profile；实际选择写入
   [creator-decision.example.jsonl](assets/creator-decision.example.jsonl) 所示 ledger。
5. 记录 suite/contract 版本与空的五轴生命周期状态。
6. 告知项目路径和最有用的创作者动作。

初始化不生成故事引擎、剧本或资产 bible。

## 确定性工具

从本 Skill 安装目录调用 `scripts/project_tool.py`；不依赖当前 CWD：

```text
python3 <short-drama-skill-dir>/scripts/project_tool.py init <project> --title <title>
python3 <short-drama-skill-dir>/scripts/project_tool.py status <project>
python3 <short-drama-skill-dir>/scripts/project_tool.py recover <project>
python3 <short-drama-skill-dir>/scripts/project_tool.py publish <project> --owner short-drama-write --artifact-id EP001:script --output episodes/EP001/screenplay.md=inputs/EP001-screenplay.candidate.md [--input <upstream-path>=<sha256> ...]
python3 <short-drama-skill-dir>/scripts/project_tool.py accept <project> --artifact-id EP001:script --decision accepted --target episodes/EP001/screenplay.md=<candidate-sha256> --evidence-artifact creator-decisions.jsonl --evidence-hash <decision-file-sha256> --evidence-record-id <decision-id>
python3 <short-drama-skill-dir>/scripts/project_tool.py review <project> --artifact-id EP001:script --verdict approve --target episodes/EP001/screenplay.md=<accepted-sha256> --verdict-owner short-drama-review --verdict-artifact reviews/EP001-verdict.json --verdict-hash <verdict-file-sha256>
python3 <short-drama-skill-dir>/scripts/project_tool.py package <project> --episode EP001 --include <accepted-path> [...]
```

`publish --output <target>=<source>` 可重复，source 必须是项目内 UTF-8
Markdown/JSON/JSONL；命令把 source 与依赖 `--input` 的 exact path/hash 写入 WAL，只发布
candidate，且只完成容器语法检查，`validation_state` 保持 `not_run`；不能同时填写 creator
acceptance 或 independent review。`accept` 由 creator
decision evidence 单独把全部 exact candidate target hash 推进为 accepted；evidence owner 固定为
`creator`。JSONL evidence 必须用 `--evidence-record-id` 唯一定位同名 `decision_id`；JSON
evidence 必须是对象；所定位记录的 `status` 或 `decision` 必须与命令的 accepted/rejected 一致。
用于 artifact lifecycle 的记录还必须声明 `decision_kind:"artifact_acceptance"`、当前
`artifact_id` 和与全部 `--target` 完全相同的 `target_hashes`；其他已接受决定不能代替本次接受。
`review` 的 verdict JSON 必须列出同一组 structured reviewed ArtifactRef；结构化 `reviewer`
至少包含与 verdict owner 一致的 `owner`、`kind`、`independent:true`，并在
`excluded_owner_skills` 中精确排除被审 artifact owner。`findings_ref` 必须是 reviewer-owned、
当前 live hash 的 canonical ArtifactRef，并指向可解析 JSONL；其中全部 open
fatal/error/blocker finding ID 必须与 `blocking_findings` 完全一致，`open_blocker_count` 再与之对齐。
`structural_validation` 必须是 `pass | pass_with_warnings | fail`，并由该 exact verdict 推进
validation 轴；结构校验未通过或有 open blocker 时不能 approve。后续 target 或任一 evidence
文件 hash 改变都要重新接受/审查。

接受时把 candidate 的 exact input map 固化为 `accepted_inputs`。任一新 candidate 发布会在同一
WAL manifest 中计算 direct/transitive stale closure：保留旧 creator acceptance 证据，但把下游
build 标为 stale、清空 validation/review readiness 并阻断 delivery。`review`/`package` 递归复验
input live hash、唯一 accepted provider、provider build/acceptance 与其自身 inputs；外部编辑或循环/
歧义 dependency 不能靠手改 lifecycle 字符串绕过。若多文件 artifact 的新 candidate 不再包含
旧 accepted/candidate target，该路径作为失效输入进入同一 stale closure；旧文件不会静默删除，
但新接受后不再拥有 accepted authority，也不能被单独打包。Publish 会递归读取 JSON/JSONL
candidate 中 canonical-looking `owner/artifact/hash` refs：指向同次 output 时 hash 必须匹配该
candidate bytes，其他 refs 必须以相同 path/hash 出现在 `--input`。遗漏或不一致在 WAL 前拒绝；
Markdown dependency 无可靠结构可推断，仍必须由 owner 显式声明。

`recover --transaction <txid>` 只处理指定事务。`package` 会重新验证 state 中保存的 creator
decision 与 independent verdict evidence，再接受当前 hash 与 accepted snapshot 一致、且五轴
delivery-ready 的 Markdown/JSON/JSONL。需要交付故事中屏显
URL 时，使用绑定 exact text/path/field/provenance/text treatment 的明确 exception 文件；
其他 URL 默认阻断。

## 状态与下一步

用创作者语言说明：

- 已存在的 accepted source；
- provisional、stale、blocked、待创作者接受的内容；
- 当前可并行进入的分支；
- 推动用户所求结果的最小动作。

除非用户要求诊断，不打印 hash、transaction ID、schema 内部或原始 state dump。
五个生命周期轴彼此独立：build、validation、creator acceptance、independent review、
delivery gate；不得用一个 `accepted` 冒充全部。

## 恢复与修订

恢复用户所问 owner 内最早未完成的操作，而不是全项目最早阶段。变更 accepted truth 前：

1. 指明 owner skill；
2. 展示拟议的语义变化；
3. 列出精确 stale closure；
4. 在需要时取得创作者接受；
5. 交给 owner 修改，并对新 hash 重新审查。

无 COMMIT 的不完整事务回滚到已保存 prior；有 COMMIT 的不完整事务前滚到 candidate 并
补齐状态。恢复必须先读后写、可重复运行，未知外部字节必须进入 conflict 而不是被覆盖。

## 交付

先路由到 `$short-drama-review` 校验，再在 delivery gate 就绪时打包。只包含 accepted
剧本、manifest、提示词、审查、创作者 notes 与 checksums。排除二进制媒体、非公开输入、
机器状态、绝对路径、凭据、非公开来源材料和未批准草稿。

## 边界

- 只使用宿主 agent 的文本推理；不调用媒体生成或服务 API。
- 运行时不检索外部或非公开生产来源。
- 不把别处见过的案例提升为创作定律。
- owner 不自批。
- 语义冲突不静默修复。
