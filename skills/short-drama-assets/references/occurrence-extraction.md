# 从剧本提取资产出现记录

## 目的：保存证据，不抢先下结论

Occurrence 是“某段剧本在某处要求了什么”的证据记录，不是资产身份本身。先提
occurrence，后判身份，可以避免两种常见返工：把同一角色的几套衣服拆成几个人，
或把两个不同的人因为同一称谓误并为一人。

**`structural_invariant` AST-01：** 每条 occurrence 指向准确的 screenplay
artifact/hash/field、block ID 与 scene。行号只能辅助阅读，不能代替稳定来源。

## 按 block 扫，而不是跑“名词识别”

逐个生产相关 block 做六问：

1. **谁/什么需要被看见或听见？** 角色、群体、动物、地点、可操作道具。
2. **以什么存在方式出现？** `on_screen`、`voice_only`、`represented`
   （照片/屏幕/画像）、`mentioned_only`。
3. **此刻可观察到什么？** 只摘剧本已给出的外观、状态、位置和动作后果。
4. **什么必须被生产实现？** 服装、伤污、可读字、内容物、功能状态、关键入口等。
5. **它为何重要？** 识别、行动、信息揭示、关系/权力、交接、气氛或普通布景。
6. **它从哪里来、要去哪里？** incoming、同场变化、outgoing；若有变化，预留
   continuity-delta pointer，不在 occurrence 中另造第二份真相。

动作句常同时含多类 occurrence。例如合成剧本块：

> 顾禾推开旧渡站值班室的北门，把带裂口的白瓷号牌放进铁皮匣。匣盖内侧写着
> “潮位 7”。

至少得到：角色顾禾（出镜）；地点旧渡站值班室（北门是固定空间锚点候选）；白瓷
号牌（裂口状态）；铁皮匣（打开且出现可读内文）。不是把“北门”“裂口”“潮位”
各自建成资产。

## 事实分层

Occurrence 中的内容按权威分开：

| 内容 | 数据角色 | 写法 |
|---|---|---|
| block/scene 指针 | `source_ref` | owner artifact/hash/field；不复制权威文本 |
| 剧本明示的可见事实 | `derived_projection` | 简短摘义并指回具体字段 |
| 拟绑定对象 | `derived_annotation` | occurrence 只保留提案；decision artifact 单向引用 occurrence 并拥有决定 |
| continuity delta | `source_ref` | 指向 assets-owned delta 的 artifact/hash/field |

不要把推测伪装成 visible fact。可安全演绎的结果也注明性质，例如“匣盖被推开”可
投影为 `open`；“顾禾很内疚”不能由低头直接升级为资产事实。

Occurrence 不用整文件 hash 反向引用 decisions；决定尚未创建时只写
`decision_locator`，决定创建后由 decisions→occurrences 的 canonical ref 证明来源。
同理，未来 continuity delta 使用 locator。这样保持单向 authority DAG，避免两个文件
互相包含对方最终 hash。

## 称谓、代词和匿名对象

**`reviewed_invariant` AST-02：** 只要两个候选都合理，就不绑定。

- 原文“她”且 block 内无唯一先行项：保留 `surface_form: 她`，decision 为
  `unresolved`，列候选和所需确认。
- “穿雨衣的人”后来被明确叫出姓名：可提议 reconcile，但必须展示前后 block
  证据；不是因为服装相同就自动等同。
- “另一把钥匙”说明与上一把不同，但还不知道是否已有 PROP ID；先建立独立
  occurrence，不能复用上一把。
- 同一人被职务、关系、名字交替称呼：alias 只有创作者接受后才进入 Character。
- 群体称谓先按生产用途处理。无个体连续性的“候车乘客”可以是群组或 set
  dressing；后来接过关键道具的个体应独立 reconcile。

不要为了“让流水线继续”做低置信度猜测。未决项的价值正是保护下游不把错误身份
放大成参考图、分镜和视频提示词。

## 出现不等于视觉资产

- `voice_only` 需要 Character/声音事实，但本场可能不需要 Look binding。
- `represented` 可能需要同一 Character 的特定历史 Look，也可能只是不可辨识照片；
  看剧情要求，不默认露脸。
- `mentioned_only` 通常只保留故事追踪，不触发图片资产；若台词指定观众必须读到
  某份文件，它实际上还有 Prop occurrence。
- 环境中普通桌椅可标 `set_dressing`，除非它们承担动作、识别或连续性。

**`craft_default` AST-06：** 能改变识别、复用、prompt、镜头或连续性的事实才进入
资产记录。覆盖此默认时写明制作原因，例如“品牌布景需要逐件批准”。

## 状态摘取要点

### 角色

记录本次 Look 线索、伤污/湿度、伪装、携带物和故事功能。不在这里发明脸型、年龄、
颜色搭配；bible 缺失的识别锚点留给 creator decision。

### 地点

记录地点称谓、内外、可见分区/入口/固定锚点，以及剧本明示的时段、天气、光源。
“低机位看门”是 shot 意图，不是新地点事实。

### 道具

记录形制/材料/尺度线索、唯一标记、所有者/所在、手、开闭/启停、破损、内容物和
可读文字。文字保持原样并注明文本政策候选，不能私自润色剧情证据。

## 完整性检查

- 对 index 中每个生产相关 block 都给出已提取或 `no_asset_change` disposition；
- 同一 block 的动作前后若改变状态，至少能找到 delta 候选；
- 同一实体在不同表面称谓下未被静默重复或合并；
- 只提及的名词不会无缘无故膨胀视觉资产表；
- 每个 proposed binding 都仍是提案，直到 decision 被 creator 接受。
