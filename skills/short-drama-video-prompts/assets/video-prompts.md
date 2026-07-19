# `video-prompts.md` 可复制输出模板

这是 accepted motion specs 的缓存视图，不是 storyboard authority。复制引用块即可；元信息帮助核对边界。

```markdown
# EP<编号> · 视频提示词

> 来源：`motion-specs.jsonl` accepted snapshot `<hash>`
> 配方：`motion-generic@<version>` · rendered `<hash>`
> 范围：仅提示词，不生成视频/音频，不调用媒体服务

## `SHOT-<id>` · <镜头目的短句>

- **Motion**：`MOTION-<id>`
- **Start frame**：`KEY-<id>` @ `<hash>`
- **时长（只读）**：`<seconds>s`
- **边界核对**：`end match | mismatch | unrealized`
- **声音引用**：`<dialogue/VO/OS/SFX ids>`
- **注意**：<feasibility warning / owner revision request；无则写“无”>

### 可复制通用提示词

> 从<最小 start anchor>开始。<按因果和物理顺序写主体动作>；<触发—处理—选择—landing 的可见表演变化>。摄影机<有动机的 lock/move、节奏和终点>。<必要环境运动>。对白/声音：<exact text/ref、delivery、声源与层级>。在<accepted duration>内<节奏安排>，最终<逐项实现 accepted end，不写下一镜>。

### 只读 end report

- **位置/姿态**：<reported → source: match?>
- **目光/双手/持物**：<reported → source: match?>
- **可见状态**：<reported → source: match?>
- **下一镜**：仅比较 `<next shot start ref>`，未改写

---
```

每个 authored shot 独立一节，即使将来由外部工具批量打包也不合并源边界。若自然语言修改涉及 duration/end/dialogue/next shot，展示 owner revision request 而不是改本文件掩盖。
