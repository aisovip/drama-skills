# 资产连续性与 Delta

## 边界匹配 (`CON-01`)

对相连镜头，逐字段比较已接受的出镜状态与下一镜头的已接受起始状态。
只有上游 owner 已记录转变，或显式 owner revision 处于开放状态，不一致才是
可解释的；不得靠 motion 措辞悄悄“补过去”。

## Ledger 与 delta 的区别

- **Ledger/state** 回答某个边界“现在是什么状态”。
- **Delta** 回答“什么从 before 变到 after、为何变、何时生效、影响谁”。

不要每场复制完整 bible；只记录下游会依赖的状态和变化。这样既能发现瞬移，也能在
剧本修改后准确标记 stale，而不是重做全项目。

## 谁拥有什么

Assets 拥有身份/variant 与场景级资产状态变化，例如 Look 何时切换、Prop 所有权转移、
Location 光态从正常到停电。Develop 拥有 planned story-state；Screenplay 拥有已写出的
知识、信念、目标、关系/权力、情绪变化及其故事含义。Assets ledger 只引用
这些权威字段，不得在 `after` 中另写一个新的 story-state。
Storyboard 独占每个 shot 的 start/end pose、position、gaze、hands、held props 和可见
continuity；assets 可以引用这些边界，不能另写一套相冲突的手位和走位。

**`structural_invariant` CON-04：** 每条 delta 都有 before、after、cause/source、
effective range，以及已存在的 `affected_binding_refs`/未来的
`affected_binding_locators`。没有变化不能只写“更新了”。

**`structural_invariant` CON-06：** `affected_binding_refs` 覆盖所有已存消费者；
尚未建立的消费者在真正发布前只是 locator。

## 应追踪的五组状态

1. **角色故事投影**：知识、信念、目标、关系/权力、情绪。仅在影响后续行为/
   审稿时追踪；每项都指向 develop/write 权威记录，不是 asset-owned delta。
2. **角色可见**：exact Look、伤势、污湿，以及场景级携带物。镜内姿势交给 shot。
3. **地点**：Location/View、可用入口、时段、天气、光态、关键陈设。
4. **道具**：exact State、owner/holder/location、状况、内容物、可读文字。
5. **交接**：上一场/集 outgoing 到下一场/集 incoming，及依赖这些状态的 prompt/shot。

**`craft_default` CON-03：** 只跟踪后续可能引用的事实。顾禾鞋带颜色若无识别/动作
意义，不必在每场重复；她带走的唯一号牌必须进入 outgoing。

## 写 delta 的步骤

1. 在 occurrence 中发现显式变化或边界不一致；
2. 读取上一 accepted state，绝不从下游 prompt 反推；
3. 写一个单义 before/after；复合事件可拆成同一 cause 下的多条 delta；
4. 引用导致变化的 block/hash/field；
5. 声明从哪个 block/scene/episode 生效，到何时结束或 `open_ended`；
6. 已存在的消费者写 canonical `affected_binding_refs`；尚未生成的
   shot/prompt 只写 `affected_binding_locators`，不伪造 hash/ref；
7. 比较下一 linked start，匹配或显式 reconcile。

### “未知”不是“恢复默认”

上一集结尾人物仍带伤，本集没提伤势，不能自动恢复无伤。保留 last known state，创建
`unresolved` continuity question：是仍带伤、发生了有意省略的治疗，还是剧本遗漏？

### 知道事实 ≠ 知道对方已知道

身份/秘密场景至少区分：A 是否知道事实、B 是否知道事实、A 是否知道 B 已知道。
如果 incoming 已声明“双方互知身份”，就不能在 handoff 把“他确认对方认出自己”
当成本集新 reveal。要么修 incoming，要么重新定义本场改变的信念/策略。

### 原因存在不等于原因合理

引用了一个 block 只证明有来源，不能机械证明语义成立。例如“灯闪了一下”不足以解释
整栋渡站永久断电。**`reviewed_invariant` CON-02：** 独立 reviewer 用剧本证据判断
伤势、知识、所有权、天气和光态变化是否可信，不能靠字段非空放行。

## 合成状态链

SC004 开始：顾禾穿 `LOOK-GUHE-RAIN`；铁皮匣闭合，号牌在内；值班室灯亮。

1. 她开匣取牌：匣 `closed/full -> open/empty`；号牌 `inside_case -> right_hand`。
2. 她把号牌交给魏叔：号牌 `Gu He/right_hand -> Wei/right_hand`，cause 指向交付动作。
3. 配电箱跳闸：View `normal_night -> blackout`，直到维修或集末仍 open-ended。
4. 暴雨从破窗打湿雨衣右肩：角色 visible delta 变湿；若跨集/需参考图再升 Look。

Outgoing 至少声明：魏叔持号牌、铁皮匣空且开、值班室断电、顾禾雨衣右肩湿。下一集
若直接写顾禾手持号牌，必须有归还 delta 或 creator-owned 修订，不能静默“对齐”。

## 非线性时间与有意断裂

蒙太奇、省略、梦境、主观画面可以不遵守普通邻接，但要显式声明 discontinuity type、
进入/退出边界和哪些状态仍可信。这是 **`taste_option` CON-05**，不是逃避记录的理由。
闪回不会重写当前时间线 ledger；它在自己的 timeline branch 中使用相应历史 variant。

## 修订与 stale 传播

- 改了伤势开始 block：stale 该 Look/delta 及依赖它的 prompt、shot、motion、review；
- 改了 Prop 显示名但 ID 和事实不变：通常只更新显示投影，不重做无关分镜；
- 改了 shot framing：不 stale assets；
- 改了 screenshot/prompt 文案：不反向改写 accepted state。

## 交接检查

- 每个 linked end 与 next start 相等，或有明确 owner revision；
- transfer 同时解释 from/to，物件不会在两人手里复制；
- injury/look/weather/light 不会无原因复位；
- contents state 与 character knowledge 分开；
- delta 的有效范围覆盖所有依赖镜头且不提前生效；
- `affected_binding_refs` 覆盖所有已存在的 prompt/shot/motion consumer；修订时
  先重算实际消费者，不只沿用旧清单；
- outgoing 足以让下一集继续，不依赖创作者脑内记忆。
