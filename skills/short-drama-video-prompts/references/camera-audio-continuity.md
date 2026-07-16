# 摄影机、环境声音与只读连续性

## 摄影机合同

- `VID-06` — locked 与 moving 指令不得同时统治同一区间，除非明确的
  transition 将两段分开。
- `VID-07` — locked/moving 的选择，以及 audio/lip-sync 细节量，都是从
  production profile 继承的 `taste_option`。

## 相连边界 (`CON-01`)

Motion end report 与下一 accepted shot start 必须一致，否则指明用于协调的
上游 owner revision。不要用流畅的动态措辞把连续性矛盾正常化。

## 目录

1. 摄影机为什么动或不动
2. Camera contradiction
3. 环境运动
4. 对白、口型与声音
5. 只读边界与修订路由

## 1. 摄影机为什么动或不动

Camera behavior 要回答“观众注意为什么在此刻改变”。常见动机：

- **reveal**：新信息进入视野；
- **pressure**：距离收紧让压力增大；
- **alignment**：从旁观转向贴近某角色立场；
- **relationship**：重新组织两人距离/权力；
- **transition**：把注意交给 accepted end 或出口。

没有动机时 lock-off 也是积极选择。镜头稳定地等待角色完成一次艰难决定，可能比装饰性环绕更有力。

### 描述 movement

一次 movement 至少写：

1. 起始 framing/相对位置（来自 shot/keyframe）；
2. 何时、因何开始；
3. 路径/方向与节奏；
4. 跟谁/揭示什么；
5. 结束 framing 或空间关系（必须在 storyboard 边界内）。

“轻微推近”若不说明触发和落点，仍然含糊。“镜头在他把钥匙放上桌时开始短促推近，钥匙落下后停在双手与钥匙的近景”才有可执行注意路径。

- **`craft_default`**：一个 authored shot 优先一个主要 camera idea；细小修正服务同一 idea。
- **`reviewed_invariant`**：move 必须与 shot purpose、表演和 blocking 相容，不能穿过墙体或错过关键动作。
- **`taste_option`**：locked、handheld、dolly、pan/tilt、角色跟随或静观均可，由 visual direction 决定。

## 2. Camera contradiction

### 同一区间的显式冲突

- `locked-off` 同时又要求 pan/dolly/handheld 漂移；
- “机位完全不动”同时“跟随角色穿过房间”；
- 同一时间既向左 pan 又向右 pan，且没有反向 transition；
- camera endpoint 与 accepted shot framing/end boundary 显式不相容。

这些可在规格的 interval/behavior 中确定比较，属于 **`structural_invariant`**。修复是选择一个行为或写清时间 transition：

```text
0.0–1.2s locked：等待她抬眼；
1.2–4.0s slow push-in：从双人中景收至她的头肩，终点保持既定轴线。
```

这里不是同时 lock 和 move。若 transition 改变 shot 已接受的 camera design，仍需 storyboard 同意。

### 非冲突但可能过载

pan 同时微调焦点、handheld 带自然呼吸、dolly 配合轻微 tilt 未必矛盾；是否太复杂由 reviewer 结合 purpose 判断，不能靠 camera 动词计数硬挡。

### 切镜边界

“切到门外、再切回特写”是新的 editorial cut，不是 camera movement。保持各 authored shot 独立；provider 批处理只是交付格式，不能把多个 source shot 融成一个不可审查 motion。

## 3. 环境运动

环境 motion 应来自连续性与 shot purpose：风、雨、蒸汽、布料、机械、群演、光影变化、液体/尘埃对主体动作的物理响应。

选择规则：

- 与主体接触或提供 cue 的优先；
- 能加强焦点但不抢戏的保留；
- 已由 reference frame 静态承载、且不会变化的省略；
- 未在 accepted state 出现的天气、火、破坏、群众事件不得为“丰富画面”发明。

**`craft_default`**：每镜只写少量 story-relevant environment motion。**`reviewed_invariant`**：环境变化不能造成新的故事事实或 continuity teleport。

## 4. 对白、口型与声音

### 精确引用

Motion spec 存 dialogue/VO/SFX/audio 的 artifact/hash/field refs；copyable prompt 可呈现 exact accepted line 或引用标记，取决于交付需要，但不得改字、增删、交换说话人或把对白改 VO。

若 source 写 `[VO]`、`[OS]`、`[SFX]`，保持声源性质：

- dialogue：画内说话者与口型/表演相关；
- VO：声音不要求当前画面口型；
- OS：说话人不在画面或不见口部，保持空间方向；
- SFX：说明事件与声源/时点；
- ambience：连续底声，不能遮蔽剧情必需对白；
- music：写叙事功能、进入/退出与层级，不用曲名模仿未授权作品。

### Delivery 与 lip-sync

可以描述速度、音量、气息、停顿、打断、称呼重音、口型意图，但不得修改台词文本来配动作。

- **`craft_default`**：对白主导镜头减少竞争性动作/camera，让 reaction 有落点。
- **`reviewed_invariant`**：delivery 必须符合角色 agenda 和表演弧；不能把威胁台词提示成真诚道歉，除非剧本有反讽依据。
- **`taste_option`**：严格口型、近似同步、VO 优先、现场感/配乐密度由 production profile 决定。

### 音频矛盾

- exact dialogue 同时要求“全程无人说话”；
- 同一 SFX 既在动作前触发又由该动作产生；
- source 是 VO，却要求清楚同步画内口型；
- accepted quiet scene 被新增爆炸声改变故事。

Resolvable ref/显式否定可结构检查；delivery 是否语义背离则要 reviewer 证据。

## 5. 只读边界与修订路由

### Motion 可以改

- 同一边界内动作的可执行路径与细节；
- accepted emotional change 的外显方式；
- 既定 camera idea 的节奏/触发实现；
- accepted audio 的 delivery、空间化和层级；
- 不改故事事实的环境微动；
- prompt 的语言经济性。

### Motion 不可以改

- shot duration、start/end pose/position/gaze/hands/held props；
- location/View、asset variant、axis/next-shot state；
- screenplay action fact、dialogue/VO/SFX 文本或说话人；
- 增删 editorial cut；
- 连续性中谁知道什么、谁拥有物件、伤势/天气/光线状态。

### Revision request

```markdown
- **请求 owner**：`storyboard | write | assets`
- **source evidence**：artifact/hash/field
- **当前边界**：精确值
- **motion 需要**：期望变化与原因
- **影响**：purpose/feasibility/continuity
- **建议**：split | extend | reblock | amend dialogue | reconcile asset
- **未执行**：列明保持 byte-identical 的 owner files
```

Video-prompts 可以提议，不能应用。若 reported end 不同于 source end：先判断是 prompt 没实现（video-prompts 修）还是创作确需新边界（storyboard 修）；无论哪种都不把 reported end 当成下一镜 authority。

### Handoff 核对

逐字段比较 motion end report 与 shot continuity out；next shot 仍直接读取 storyboard-owned start。Match 才是实现证据，不能用一句“保持连续”代替 position/gaze/hands/prop 等关键字段核对。
