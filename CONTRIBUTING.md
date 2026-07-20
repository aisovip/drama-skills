# 贡献指南

感谢参与短剧技能套件。本项目遵循“知识与做法优先”：能力尽量写入 `SKILL.md` 工作流
和 `references/` 参考资料，脚本只保留字节哈希、稳定索引和清单等确定性工作。

## 修改原则

1. **知识与做法优先**：新增能力先考虑写成参考资料或 `SKILL.md` 工作流步骤；
   只有智能体不应徒手完成的确定性工作（字节级哈希、稳定索引）才写脚本。
   不要把编辑/创作判断写成规则代码。
2. **规则分级**：所有规范都要归入 `structural_invariant` / `reviewed_invariant` /
   `craft_default` / `taste_option` 四级；不得把统一的字数、比例、数量配方设为
   质量门槛。可迁移知识在 `skills/short-drama/references/knowhow-index.md` 注册
   稳定 ID。
3. **所有权与独立审查**：每个产物只有一个负责技能；负责人不能审查自己的产物。
4. **来源边界**：仓库不得包含非公开项目内容、内部标识、私有网址、供应商任务
   或媒体文件；示例一律合成改写。边界测试会检查这些要求。

## 修改后必跑

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -B -m unittest discover -s tests -v
ruff check --no-cache .
python3 tools/verify_suite.py skills/short-drama
```

改动 `skills/` 下任何文件后，需重建套件清单（会同步重写 7 个 `suite-ref.json`）：

```bash
python3 tools/update_suite_manifest.py skills/short-drama
```

## 提交约定

- 一个合并请求只聚焦一件事；`SKILL.md` 与配套参考资料放在同一个合并请求中。
- 提交信息说明“哪个技能的哪类知识或确定性工作”发生变化。
- 新增参考文件必须能从负责技能的 `SKILL.md` 按需打开。
