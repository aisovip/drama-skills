# Prop / State 设计

## 道具不是名词表

只有会被识别、操作、传递、读取、揭示或保持连续性的物体，才值得成为受管道具。
普通背景物可保留为 `set_dressing` occurrence；一旦角色拿起它打开秘密、它跨场转手，
就要能以稳定身份追踪。

## Prop：持续身份

Prop 保存不随本次动作轻易改变的识别信息：

- 大小/尺度参照、基本形制和部件关系；
- 主要材料、表面工艺、持久磨损；
- 原本功能和操作方式；
- 序列号、缺口、纹章等永久唯一标记；
- 同款多件时的个体区分或 class/quantity 策略。

“重要文件”“神秘盒子”“高级质感”只是剧情/氛围标签，不能保证再次生成时认出同一
件物体。反过来，也不要补写剧本没给的品牌和装饰。

## State：此刻怎样

State 记录可变而需跟踪的事实：

- owner、holder、left/right hand 或具体 location；
- 完好/裂损、干湿/污渍、开/闭/锁、开机/关机；
- 内容物及其是否已被看见；
- 可读文字/图形的当前版本；
- 组装、封条、消耗量或功能状态；
- cause 与有效范围。

**`craft_default` AST-03：** 同一物体的转手、开合、破损、内容与文字变化优先做
State/delta，不重复创建 Prop。

## 个体、同款与集合

- 两枚外观相同的白瓷号牌分别被交换、藏匿：创建两个 Prop，因其所有权链必须独立；
- 柜台上的一叠普通空白便签仅作背景：可用 class/quantity，不必逐张 ID；
- 一把钥匙从顾禾手中转到值班员手中：仍是同一 Prop，State 改 owner/hand；
- “另一把钥匙”明确不是上一把，但尚不知对应哪个已有 ID：新 occurrence + unresolved，
  不能偷懒复用。

个体化程度是 **`taste_option`**，选择依据故事追踪与制作需求，而不是总数最少。

## 可读文字政策

每个出现文字的 Prop 明确选一种：

1. `exact_readable`：剧情要求观众读到；保存准确字符、语言、大小写/标点及来源；
2. `graphic_only`：需要标签/印记形状，但不要求可辨文字；
3. `no_readable_text`：画面不应出现可读字；
4. `pending_creator_text`：剧本要求文字但内容未定，阻断依赖它的 prompt。

文字是剧本事实时，assets 只保存政策与 source pointer，不自行润色。后续 prompt 不能
同时要求 `exact_readable` 和全局 `no_text`。

若剧情出现 URL、号码、合同内容等敏感屏显，须有 provenance、on-screen text 声明和
creator delivery acceptance；不能把本地引用路径或内部地址带入交付。

## 内容物与知识是两条连续性

盒中始终有号牌，是 Prop contents state；顾禾在打开盒子后才知道号牌存在，是角色
knowledge delta。不要因道具早已装有物品，就让人物提前拥有知识。相反，镜头没展示
内容物不代表它凭空消失。

## 合成例：铁皮匣

`PROP-TIN-CASE`：手掌至小臂长度的扁长黑铁匣；铰链盖；右前角永久凹陷；用途为保存
渡站号牌。`“潮位 7”` 写在盖内，政策 `exact_readable`。

- `PSTATE-TIN-CLOSED-BADGE-IN`：匣闭合，白瓷号牌在内，位于柜台下层；
- SC004 顾禾取出：delta 将 `closed -> open`、`contents: badge -> empty`，号牌获得
  自己的 holder state；
- 匣盖内文在开启后才可见，但文字不是这时才“产生”。观众/角色知道它则另写
  reveal/knowledge delta。

反例：开匣后创建 `PROP-OPEN-CASE`、拿出号牌后再创建 `PROP-EMPTY-CASE`。这样无法
表达同一匣子的状态演进，也容易让不同镜头各拿一个假副本。

## 检查问题

- 去掉 owner、开合和内容物后，Prop 是否仍有可识别的形制/尺度/材料？
- 同一物体的 state 能否沿 source block 逐步演进，而非瞬移？
- 同款多件是否因故事追踪需要而正确区分？
- 可读文字是否精确、来源明确、与 no-text 政策不冲突？
- 角色手里拿的物体是否既出现在 Prop State，也在后续 storyboard boundary 被引用？
- 不可逆功能改造若成为新 Prop，是否保留 derived-from 与 creator decision？

**`reviewed_invariant` AST-04：** reviewer 应指出身份与状态混写、无证据的内容/文字、
或无法解释的转手；简单关键词匹配不能替代这项判断。
