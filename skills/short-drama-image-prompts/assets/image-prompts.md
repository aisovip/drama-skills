# `image-prompts.md` 可复制输出模板

此文件是 accepted spec + recipe hash 的缓存视图。元信息用于审计；只复制引用块内的通用提示词。不要手写供应商参数。

```markdown
# EP<编号> · 资产图片提示词

> 来源：`image-prompt-specs.jsonl` accepted snapshot `<hash>`
> 配方：`<recipe>@<version>` · rendered `<hash>`
> 范围：仅提示词，不生成图片或调用媒体服务

## `<display name>` · `<purpose>`

- **Spec**：`IMG-<id>`
- **绑定**：`<asset-id>` + `<variant-id>`
- **用途**：<后续复用目标>
- **文字来源政策**：`exact_readable | graphic_only | no_readable_text | pending_creator_text`
- **本次呈现**：`readable | symbolic | blank | postproduction`（附 source → treatment 映射）
- **注意**：<未阻断的 warning / creator override；无则写“无”>

### 可复制通用提示词

> <自然中文正文。用途/主体与区分性锚点在前，状态、构图、空间/尺度、材质/光线、背景、文字政策、保持/排除依次展开。不要出现字段名、hash、审查话术或生成历史。>

### 变体/编辑说明

- **相对基准**：<base variant；非 variant 可省略>
- **变化**：<observable delta；无则省略>
- **必须保持**：<preserve set；非 edit 可简写或省略>
- **连续性影响**：<accepted binding / none；非 edit 可省略>

---
```

每个 asset/version 独立一节；不要把多个互斥 Look/View/State 合成一个 copy block。若该文件与规格 hash 漂移，先走 `restore | adopt` 预览流程。
