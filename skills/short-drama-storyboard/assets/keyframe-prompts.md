# `keyframe-prompts.md` 可复制输出模板

这是 accepted `keyframes.jsonl` 的缓存视图，不是 shot boundary 或资产 authority。
每次渲染都保存输入 hashes、配方版本和 rendered hash；缓存被手改时走 restore/adopt/merge。

```markdown
# EP<编号> · 冻结关键帧提示词

> 来源：`keyframes.jsonl` accepted snapshot `<hash>`
> 配方：`keyframe-generic@<version>` · rendered `<hash>`
> 范围：单一静止瞬间；不生成图片，不写时间动作

## `SHOT-<id>` · `KEY-<id>`

- **镜头目的**：<观众此刻必须看见什么>
- **边界来源**：`SHOT-<id>/start_boundary` @ `<hash>`
- **资产绑定**：`<exact Character/Look · Location/View · Prop/State>`
- **文字处理**：`<accepted source policy -> frame treatment>`

### 可复制通用提示词

> <焦点主体与识别锚点>。<构图层级、人物/道具/空间锚点关系>。摄影机<景别、角度、镜头意图>。
> <一个可冻结的姿态、目光、双手、持物与可见表演状态>。<继承的光向、时段、天气与必要气氛>。
> <文字处理>。保持<边界与身份事实>；排除<本帧高风险漂移>。

---
```

若一句话必须靠“先/再/随后/最终”才能成立，把它移交 motion；若要改变 start boundary，
先向 storyboard owner 提 revision，不在缓存提示词中偷偷改。
