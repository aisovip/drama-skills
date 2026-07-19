---
name: short-drama-video-prompts
description: 为已接受的短剧镜头和关键帧编写或修改可复制的通用视频提示词与 motion spec。用户提到视频 prompt、图生视频动作、人物表演过程、运镜、对白口型、环境运动、镜头时长、起止状态或把分镜转成视频提示词时直接使用；只描述单个已编镜头内的运动、表演、摄影与声音，不生成视频、不调用模型或供应商 API，也不改写分镜边界。
---

# 短剧视频提示词

把 storyboard 已经决定的一个镜头，翻译成时间中可执行的动作、表演、摄影和声音。Motion 实现边界，不拥有边界。

## 进入条件与权属

- 可从已接受 shots/keyframes 直接进入，无需重新开发故事；先定位项目和唯一匹配的 sibling core。
- 读取 core 的 `references/contract-and-ownership.md` 与 `references/knowhow-index.md` 中 `VID-*`、`SHT-*`、`CON-*`。
- 输入至少包含 accepted shot、start keyframe/boundary、duration、continuity out 与 dialogue/audio refs；未接受或 stale 时退回 `$short-drama-storyboard`。
- 若 creator 明确要求全链 preview，可对 provisional 但非 unresolved 的 shot/keyframe
  写 candidate motion；保留 `authority:candidate`，禁止声称 accepted、approved 或
  delivery-ready。
- shot 的 start/end、duration、dialogue、asset bindings、next-shot state 全部只读。Motion 只拥有 ordered motion、performance path、camera/audio realization 与派生 end report。
- 视觉/声音口型等 taste 读取 `short-drama.json#/creator_authority/{visual_direction,production_profile}`；
  direct-entry 项目为 `unset` 时保留选择，不把某一默认 profile 写成已接受事实。
- 输出永远 generic-first。不得生成视频/音频、上传参考帧、创建远程执行任务、调用模型/API、轮询状态或宣称成片质量。

## 按任务加载资料

| 任务 | 必读资料 |
|---|---|
| 任意镜头 motion/prompt | [起点—变化—终点配方](references/motion-recipe.md) |
| 动作、表演、节奏或超载 | [表演弧与动作预算](references/performance-action-timing.md) |
| 运镜、环境、对白、声音、边界冲突 | [摄影声音与连续性](references/camera-audio-continuity.md) |
| 自检、独立复核、正反案例 | [审查量表与合成案例](references/review-and-fixtures.md) |
| 生产端 prompt 语法、台词绑定、负面清单 | [生产提示词语法惯例](references/production-prompt-grammar.md) |

规格使用 [motion spec 模板](assets/motion-spec.jsonl.md)；末镜或下一集记录尚未建立时参考
[terminal motion locator 示例](assets/motion-terminal.example.jsonl)；可复制交付使用
[Markdown 模板](assets/video-prompts.md)。只加载本次问题需要的资料。

## 工作流

### 1. 先写“不能动的边框”

建立只读 boundary card：

- shot/keyframe exact artifact/hash/field refs；
- duration 与 start pose、balance、gaze、hands、held props、空间关系；
- storyboard-owned end pose/state 与 continuity out；
- exact dialogue/VO/SFX/audio refs；
- shot purpose、信息/情绪变化和 next-shot handoff（只用于核对）。

任何来源冲突先停止。如果创作者要求延长时长、换结尾站位、删对白或改变下一镜开场，写 owner-specific revision request；不要在 motion 中覆盖。

### 2. 决定这个镜头真正发生什么变化

用一句话写 motion purpose：“观众在这几秒内看到/感到什么变化？”然后选择少量有因果顺序的事件：主体行动 → 可见反应/注意转移 → end realization。只加活动会稀释表演。

- `reviewed_invariant`：动作负载必须让演员有时间完成镜头的故事变化；general feasibility 由 reviewer 看证据，不用动词数或固定秒/动作公式硬挡。
- `craft_default`：短镜头优先一个 primary action，加一个必要 reaction；复杂过程请求 storyboard 拆镜或延长。
- `taste_option`：克制、爆发、停顿、喜剧节奏等取决于角色和导演意图。

### 3. 按七部分编写 motion

1. **Start anchor**：只重述开动所需的姿态、重心、目光、手、持物、空间关系。
2. **Ordered subject action**：谁先做什么、方向/路径、物理接触与先后；不要用一串“同时”。
3. **Performance arc**：触发 → 内在处理的外显迹象 → 决定/行动 → 到达 end state。
4. **Camera behavior**：一次有动机的 move，写起点、速度/节奏和终点；或明确 lock-off。
5. **Environment/audio**：只写有剧情和连续性依据的环境运动、对白/VO、环境声、SFX/音乐意图。
6. **Timing**：用阶段/顺序为主；需要精确时间时，其显式段落总和不得超过 duration。
7. **End report**：报告实际描述将如何落到 storyboard-owned continuity out；它是 comparison projection，不是新权威。

### 4. 使用参考帧经济性

如果绑定 frame 已承载人物外貌、服装、场景构图和光线，正文聚焦“从此刻开始怎么变”。只重复动作执行易漂移的局部事实，如“右手仍握住铜夹”。不要倾倒完整人物/场景 bible，也不要用“与参考一致”替代必要的 start anchor。

### 5. 检查冲突与单镜头边界

- `structural_invariant`：明确 segment timing 不超 duration；同一时间区间不能既 locked 又 pan/dolly/handheld，除非写清 transition；refs 必须解析；end report 必须匹配 source end。
- `reviewed_invariant`：动作物理可行、表演弧可见、摄影有动机、没有语义发明。
- `craft_default`：环境和摄影只支持注意、压力、揭示、结盟或转场，不用来装饰每一镜。
- `taste_option`：lock/move、焦段语汇、口型精度、音乐密度由生产 profile 决定。

一个 authored shot 保持一个 editorial boundary。不要在一条 prompt 里偷藏多次切镜；批量打包也不改变源 shot 的独立可审查性。

### 6. 预览、接受与发布

先向创作者展示 boundary 摘要、动作/表演顺序、camera/audio 选择、时长警告和 copyable prompt。接受后写：

- `episodes/<EP>/storyboard/motion-specs.jsonl`：motion 权威字段 + 只读 source refs；
- `episodes/<EP>/storyboard/video-prompts.md`：accepted spec + recipe hash 的缓存视图。

自然语言改 prompt 时先给 spec diff 与重渲染预览；若改动触碰 shot/write owner，保持当前文件不变并路由 revision request。跨文件发布遵循 core 事务恢复流程。

## 完成标准

- prompt 从精确 start anchor 出发，以明确顺序实现 accepted end，不改变 duration/dialogue/下一镜；
- 表演有触发、处理与可见变化，动作量可行，摄影与环境/声音服务 shot purpose；
- 参考帧已知外观不被重复淹没，generic prompt 可独立复制；
- 本地结构检查后交 `$short-drama-review` 做证据化 feasibility/语义复核；
- 没有媒体文件、API/provider/task 字段、远端 ID 或“视频已生成”声明。
