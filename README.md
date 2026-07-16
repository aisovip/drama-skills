# Drama Skills

中文 | [English](README_EN.md)

基于文件系统的短剧创作 Agent Skill 套件，兼容 Claude Code、Codex 等支持
Agent Skills 的运行时。它把短剧生产中的可迁移 know-how 沉淀为工作流、参考资料、
模板、示例和审查量表，覆盖从故事开发到文本交付的完整链路。

本仓库只生成和管理文本、Markdown、JSON 与 JSONL：剧本、资产决策、图片提示词、
分镜/关键帧提示词、视频提示词和审查证据。它不生成图片、视频或音频，也不调用媒体
生成服务。

## Skills

| Skill | 职责 |
|---|---|
| `short-drama` | 初始化、路由、状态、异常恢复、接受/审查生命周期与交付 |
| `short-drama-develop` | 故事承诺、故事引擎、系列弧与分集地图 |
| `short-drama-write` | 单集契约、因果节拍、可拍剧本与稳定索引 |
| `short-drama-assets` | 人物/造型、地点/视图、道具/状态与连续性决策 |
| `short-drama-image-prompts` | 资产图片提示词与文字处理策略 |
| `short-drama-storyboard` | Coverage、镜头、冻结关键帧及空间边界 |
| `short-drama-video-prompts` | 表演、动作、运镜、声音和起止状态视频提示词 |
| `short-drama-review` | 结构校验、证据化审查、修订请求与独立 verdict |

## 安装

八个目录必须保持 sibling 布局。复制或链接到宿主的 Skills 目录：

```bash
# Claude Code
mkdir -p "$HOME/.claude/skills"
for skill in skills/*; do
  ln -s "$PWD/$skill" "$HOME/.claude/skills/$(basename "$skill")"
done

# Codex
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"
for skill in skills/*; do
  ln -s "$PWD/$skill" "${CODEX_HOME:-$HOME/.codex}/skills/$(basename "$skill")"
done
```

已存在同名 Skill 时，先移除旧链接或选择其他安装位置，不要混装不同版本。安装后从
`$short-drama` 开始；具体任务也可以直接调用对应 Skill。

## 工作流

```text
故事开发（可选） -> 单集剧本 -> 资产决策
                              |-> 资产图片提示词
                              |-> coverage -> 镜头 -> 关键帧 -> 视频提示词
                                                        |
                                              独立审查 -> 文本交付包
```

图片提示词与 storyboard 在资产接受后可以并行。现成剧本可以直接进入剧本规范化或资产
拆解，不需要补造故事开发文件。生成候选、创作者接受、独立审查和交付是不同权限，不能
用一个 `accepted` 状态代替。

核心确定性命令：

```bash
python3 skills/short-drama/scripts/project_tool.py init <project> --title <title>
python3 skills/short-drama/scripts/project_tool.py status <project>
python3 skills/short-drama/scripts/project_tool.py recover <project>
python3 skills/short-drama/scripts/project_tool.py publish <project> --owner <skill> --artifact-id <id> --output <target>=<source>
python3 skills/short-drama/scripts/project_tool.py accept <project> --artifact-id <id> --decision accepted --target <path>=<sha256> --evidence-artifact creator-decisions.jsonl --evidence-hash <sha256> --evidence-record-id <decision-id>
python3 skills/short-drama/scripts/project_tool.py review <project> --artifact-id <id> --verdict approve --target <path>=<sha256> --verdict-owner short-drama-review --verdict-artifact <verdict.json> --verdict-hash <sha256>
python3 skills/short-drama/scripts/project_tool.py package <project> --episode EP001 --include <approved-path>
```

`publish` 使用可恢复的写前日志和快照。中断后先运行 `recover`；遇到外部编辑冲突时会
保留原字节并阻断，不会静默覆盖。接受会冻结 candidate 的 exact input hashes；上游发布新
candidate 时，同一 WAL 事务会把直接和传递下游标为 stale。`review` 与 `package` 还会递归
复验这些 inputs，所以上游被外部编辑或依赖 owner 不唯一时也不能交付旧投影。多文件
artifact 重发时，从 target set 移除的旧路径也会使依赖它的下游 stale；旧文件原字节保留，
但新接受后不再拥有 accepted authority，不能直接交付。JSON/JSONL candidate 中每个 canonical
ArtifactRef 必须对应同次 output 的 candidate hash，或出现在 exact `--input` map 中；遗漏或
hash 不一致会在写 WAL 前拒绝。Markdown 的非结构化依赖仍由 owner 显式列为 `--input`。

## 验证

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
ruff check --no-cache .
cache_dir="$(mktemp -d)"
PYTHONPYCACHEPREFIX="$cache_dir" python3 -m compileall -q skills tests
rm -rf "$cache_dir"
python3 skills/short-drama/scripts/verify_suite.py
```

每个 Skill 还应通过 `skill-creator` 提供的 `quick_validate.py`（如宿主提供）。套件清单由
`skills/short-drama/scripts/update_suite_manifest.py` 在发布前统一重建。只有七个 public child
Skill 根目录的 `suite-ref.json` 作为经过严格字段校验的循环外 manifest pin；其他同名文件和
pin 的额外字段都会使验证失败。
