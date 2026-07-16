# Contributing

感谢参与 Drama Skills。本套件是"knowhow 优先"的 Agent Skill 集合：能力尽量沉淀为
SKILL.md 工作流与 references 参考资料，脚本只保留确定性机制（哈希、索引、清单）。

## 修改原则

1. **Knowhow 优先**：新增能力先考虑写成 references 文档或 SKILL.md 工作流步骤；
   只有 agent 不应徒手完成的确定性机制（字节级哈希、稳定索引）才写脚本。
   不要把编辑/创作判断写成规则代码。
2. **规则分级**：所有规范都要归入 `structural_invariant` / `reviewed_invariant` /
   `craft_default` / `taste_option` 四级；不得把统一的字数、比例、数量配方设为
   质量门槛。可迁移知识在 `skills/short-drama/references/knowhow-index.md` 注册
   稳定 ID。
3. **所有权与独立审查**：每个产物只有一个 owner skill；owner 不能自批。
4. **来源边界**：仓库不得包含非公开项目内容、内部标识、私有 URL、供应商任务
   或媒体二进制；示例一律合成改写。boundary 测试会强制这些约束。

## 修改后必跑

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
ruff check --no-cache .
python3 skills/short-drama/scripts/verify_suite.py
```

改动 `skills/` 下任何文件后，需重建套件清单（会同步重写 7 个 `suite-ref.json`）：

```bash
python3 skills/short-drama/scripts/update_suite_manifest.py
```

## 提交约定

- 一个 PR 聚焦一件事；SKILL.md 与其 references 的配套改动放同一个 PR。
- 提交信息说明"哪个 skill 的哪类知识/机制"发生变化。
- 新增 reference 文件必须从 owner skill 的 SKILL.md 可达（按需加载链接）。
