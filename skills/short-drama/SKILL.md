---
name: short-drama
description: 基于文件系统初始化、继续、恢复和交付短剧项目，并把具体工作交给对应的短剧技能。用户提出“创建/继续短剧项目”“看进度/下一步”“恢复中断或不完整发布”“定点修订/交付”，或直接要求写短剧、拆资产、写资产图片提示词、拆分镜、写视频提示词、审查短剧时使用。
---

# 短剧创作路由

这是轻量项目路由，不在本技能内代写故事、资产提示词、镜头、视频提示词或终审结论。
默认使用创作者的语言；中文项目使用简洁中文呈现状态、差异、选择和下一步。

## 每次请求的起点

1. 使用用户明确路径，或从当前目录向上寻找最近的 `short-drama.json`。
2. 从本技能安装目录找到同一套件的其他技能，读取 `suite-manifest.json`；缺少技能或版本混用时先停止变更。
3. 只读 `short-drama.json` 与 `.short-drama/state.json` 摘要；不要一次加载全部创作文件。
4. 执行 `status` 或写入前先运行事务恢复。发现外部编辑冲突时保留原文件，提供
   `adopt`、`restore`、`merge` 三种处理，不静默覆盖。
5. 按创作者当前任务路由；不强制补走整条流水线。

入口、检查点、修订和交付见 [creator-workflow.md](references/creator-workflow.md)。
所有权、文件过期标记 `stale`、隐私或恢复有疑问时读
[contract-and-ownership.md](references/contract-and-ownership.md)。
意图含混时读 [routing-examples.md](references/routing-examples.md)。
只在需要把规则 ID 定位到负责技能时读
[knowhow-index.md](references/knowhow-index.md)；路由只负责分派，不代替创作技能判断。
涉及参考图可以决定什么、观众揭示时机或补拍/替代提示词时读
[reference-media-and-pickups.md](references/reference-media-and-pickups.md)。

## 意图路由

| 创作者意图 | 路由 |
|---|---|
| 开发点子、故事承诺、系列、分集地图 | `$short-drama-develop` |
| 写/改单集契约、因果节拍、剧本 | `$short-drama-write` |
| 拆人物/造型、地点/视图、道具/状态 | `$short-drama-assets` |
| 写人物/地点/道具/局部修改的图片提示词 | `$short-drama-image-prompts` |
| 做原文覆盖、镜头或冻结关键帧 | `$short-drama-storyboard` |
| 写动作/表演/运镜/声音视频提示词 | `$short-drama-video-prompts` |
| 校验、审查或发修订请求 | `$short-drama-review` |

创作者明确意图优先于名义上的“下一检查点”。C2 资产接受后，图片提示词和分镜
是平行分支；创作者只要其中一支时，不强迫等待另一支。

## 初始化

没有项目且用户要初始化时：

1. 仅确认或合理推断可逆格式默认值：标题、语言、画幅、路径；集数/时长未知就留空。
2. 复制项目模板，不覆盖已有创作者文件。
3. 建立空阶段目录和非公开输入边界。
4. 在 `short-drama.json#/creator_authority` 建立空的创作者限制、视觉方向和制作配置；
   实际选择写入 [creator-decision.example.jsonl](assets/creator-decision.example.jsonl)
   所示的决定记录。
5. 记录套件版本、契约版本与五项彼此独立的空状态。
6. 告知项目路径和最有用的创作者动作。

初始化不生成故事引擎、剧本或资产设定表。

## 确定性工具

从本技能安装目录调用 `scripts/project_tool.py`，不依赖当前工作目录：

| 命令 | 用途 |
|---|---|
| `init` | 初始化最小项目 |
| `status` | 读取生命周期与恢复摘要 |
| `recover` | 恢复全部或指定事务 |
| `publish` | 通过预写日志发布 `candidate`，不附带接受或审查结论 |
| `accept` | 用创作者决定记录接受准确的 `candidate` 目标 |
| `review` | 用独立审查结论更新校验与审查状态 |
| `package` | 复验五轴、依赖和证据后生成文本交付包 |

只有实际调用这些命令、诊断失败或核对记录格式时，才读取
[lifecycle-commands.md](references/lifecycle-commands.md) 中的完整调用示例、预写日志、接受、
审查、下游过期影响与打包约束。

## 状态与下一步

用创作者语言说明：

- 已存在且状态为 `accepted` 的来源；
- 状态为 `provisional`、`stale`、`blocked` 或待创作者接受的内容；
- 当前可并行进入的分支；
- 推动用户所求结果的最小动作。

除非用户要求诊断，不打印 `hash`、事务 ID、内部数据结构或原始状态内容。
五项状态彼此独立：构建、校验、创作者接受、独立审查和交付检查；不得用一个
`accepted` 冒充全部。

## 恢复与修订

恢复用户所问环节内最早未完成的操作，而不是全项目最早阶段。变更已确认内容前：

1. 指明负责修改的技能；
2. 展示拟议的语义变化；
3. 列出准确的下游受影响清单；
4. 在需要时取得创作者接受；
5. 交给负责人修改，并对新 `hash` 重新审查。

没有 `COMMIT` 的不完整事务回滚到已保存的上一版本；已有 `COMMIT` 的不完整事务继续到
`candidate` 并补齐状态。恢复必须先读后写、可重复运行；无法确认来源的外部改动必须标为
`conflict`，不能覆盖。

## 交付

先路由到 `$short-drama-review` 校验，再在交付检查就绪时打包。只包含状态为 `accepted`
的剧本、清单、提示词、审查、创作者备注与校验和。排除二进制媒体、非公开输入、
机器状态、绝对路径、凭据、非公开来源材料和未批准草稿。

## 边界

- 只使用当前智能体的文本推理；不调用媒体生成或服务接口。
- 运行时不检索外部或非公开生产来源。
- 不把别处见过的案例提升为创作定律。
- 负责人不能审查自己的产物。
- 语义冲突不静默修复。
