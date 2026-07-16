# 视频提示词审查量表与合成案例

## 目录

1. 审查顺序
2. 证据量表
3. 诊断目录
4. 合成正例
5. 合成反例

## 1. 审查顺序

先验证 refs、显式时长、camera interval、音频否定与 end equality，再由独立 reviewer 看 performability、action feasibility、camera motivation 和 semantic invention。Reviewer 写 finding，不改 motion、shot 或 screenplay。

Finding 必须含 artifact/hash、引用片段、影响、required fix、owner、severity、status。禁止用 prompt 长度、动词数量、固定动作/秒或“AI 味”替代证据。

## 2. 证据量表

| 维度 | 核心问题 | 必须引用 |
|---|---|---|
| Start fidelity | 第一动作是否从 keyframe/shot start 真正可接上？ | start 字段与 prompt 起始句 |
| Ordered action | actor、方向、接触、先后和结果是否清楚？ | action stages |
| Performance | 触发、处理、选择、landing 是否可见且符合 agenda？ | source beat/shot purpose + motion |
| Action budget | duration 内能否保留故事动作、对白与 reaction？ | duration、距离、台词、动作、camera |
| Camera | lock/move 是否一致，且因注意/压力/揭示而发生？ | camera interval + shot purpose |
| Environment | 是否只动了有依据的环境，未发明天气/事件？ | accepted continuity + environment |
| Dialogue/audio | exact refs、说话人、VO/OS/SFX、delivery 是否保持？ | source audio fields + prompt |
| End fidelity | reported end 是否逐项等于 continuity out？ | end report + source end |
| Economy | frame 已承载外观是否被无谓倾倒？ | reference contents + copy block |
| Shot boundary | 是否偷改 duration/end/next shot 或藏多次 cut？ | source shot + motion |

语义 finding 的修复应指出删/改哪一段 motion，或该向哪个 owner 发 revision request，而不是笼统说“动作自然一点”。

## 3. 诊断目录

| code | classification | enforcer | 默认 severity | owner | 含义 |
|---|---|---|---|---|---|
| VID_SOURCE_REF_UNRESOLVED | structural_invariant | validator | error | video-prompts | shot/keyframe/dialogue/audio ref 未解析 |
| VID_EXPLICIT_TIMING_OVERFLOW | structural_invariant | validator | error | video-prompts | 显式时间终点/非重叠总量超 duration |
| VID_CAMERA_INTERVAL_CONFLICT | structural_invariant | validator | error | video-prompts | 同一区间 lock 与 move 等显式冲突 |
| VID_END_REPORT_MISMATCH | structural_invariant | validator | error | video-prompts | reported end 不等于 storyboard continuity out |
| VID_BOUNDARY_OVERRIDE | structural_invariant | validator | error | video-prompts | motion 写入 duration/end/next-shot override |
| VID_ACTION_INFEASIBLE | reviewed_invariant | reviewer | revise | video-prompts/storyboard | 一般动作负载不可行或掩盖故事变化 |
| VID_SEMANTIC_INVENTION | reviewed_invariant | reviewer | revise | video-prompts | 新造故事、关系、知识、状态或音频事实 |
| VID_CAMERA_UNMOTIVATED | craft_default | reviewer | warning | video-prompts | movement 无助于目的/注意变化 |
| VID_REFERENCE_DUMP | craft_default | reviewer | warning | video-prompts | bound frame 已带外观却重复整本 bible |
| VID_STYLE_ALTERNATIVE | taste_option | reviewer | note | video-prompts | 表演/摄影/声音风格的非阻断选择 |

语义问题只能由 reviewer 证据化判断；不要写正则把“缓慢”“同时”或动词数量变成错误。

## 4. 合成正例

以下人物、场景、对白均为虚构合成材料。

### Accepted boundary 摘要

- `SHOT-EP001-014`，duration `5.0s`，purpose：罗静听见门外有人试锁后，选择隐藏登记簿而非立刻逃跑；
- start：她坐在检修台边，左手翻开的登记簿，右手握笔，目光在页上；后方安全门位于她右后侧；
- dialogue：画外男声 `[OS] “里面有人吗？”`；
- end：她仍坐着，左手把登记簿压在工具盒下，右手握笔停在桌沿，目光锁向右后侧安全门；
- camera：接受的单镜头、固定轴线，可在触发后轻微推进。

### 合格 generic prompt

> 从参考帧的坐姿开始：她的左手仍按在翻开的登记簿上，右手握笔，目光落在页上，右后方是安全门。门外先传来一次短促的试锁声；她的笔尖立刻停住，目光先移向安全门，但身体没有起身。画外男声问“里面有人吗？”，她屏住一拍，没有回答，左手才把登记簿平稳滑入旁边工具盒下方，动作克制，避免纸页发声；右手始终握笔，最后停在桌沿。表演由专注工作转为警觉，再落到压住恐惧后的主动隐瞒。摄影机开头保持固定，在她决定藏起登记簿时做一次很短、很慢的推进，终点仍保持既定轴线，将她的左手、工具盒和望向安全门的视线纳入同一画面。维修间底噪持续，试锁声和画外问话清楚置于门的方向，无音乐突入。5 秒内完成，结尾保持她仍坐着、左手把登记簿压在工具盒下、右手握笔停在桌沿、目光锁向右后侧安全门。

为何有效：开端只重复运动关键事实；动作按声音→接收→决定→隐藏排列；OS 不要求口型；camera 在选择时启动；结尾逐字段落到 accepted boundary，没有写下一镜。

## 5. 合成反例

### 反例 A：外观倾倒与边界改写

> 她有窄长脸、断眉、短卷发，穿墨绿工装、米白 T 恤、深色长裤和短靴，维修间墙壁每一处材料都清晰。她站起来跑到门外，把笔交给陌生人，然后下一镜已经来到街上。

Finding：reference 已携带外观而 motion 没写关键表演；更严重的是 start 从坐姿跳到站立、end 新增跑出/道具转手，并代写下一镜。修复需回到 accepted 坐姿 end；若逃跑是创作意图，向 storyboard 请求新 boundary/shot。

### 反例 B：动作超载但不能靠计数器判

> 5 秒内，她听完整句问话，翻完三页，把册子锁入抽屉，走过房间关闭两扇窗，拆下墙上话筒，打电话说两句，再回到原座位保持完全静止。

Reviewer 应引用房间距离、物件操作、对白和 landing 说明不可行；不能只说“有七个动词”。优先保留与隐藏决定有关的动作，其余删减或请求 split/extend。

### 反例 C：camera 显式矛盾

```text
0–5s：摄影机绝对锁定、没有任何移动。
1–4s：摄影机持续向前 dolly 并手持环绕角色一周。
```

同一区间的 lock/move 可结构阻断。创作者可选择 lock 或 move；若需先锁后推，写不重叠 transition。

### 反例 D：音频语义发明

> 画外问话后，突然响起爆炸，所有灯熄灭，她大喊“我承认了”。

若 source 没有爆炸、停电和这句对白，这会改变故事与 continuity。由 reviewer 引用 source 缺失与 prompt 新句给 `VID_SEMANTIC_INVENTION`，不是因关键词“爆炸”本身被正则禁止。
