# `delivery-containers.jsonl` 填写模板

每行一个交付容器对象。容器只是**已接受镜头的排布方式**：它记录哪些镜头按什么顺序装进
同一个交付单位，以及由此得出的容器时长。它不拥有镜头边界、目的、起止状态或时长——
这些仍属分镜；容器只引用它们并做加法。

只有创作者声明了分段或多镜打包的交付方式时才需要本文件；单镜交付不必创建容器记录，
`VID-13` 在那种情形下由运动规格自身的镜头时长满足。

```json
{
  "container_id": "CONT-<stable-id>",
  "status": "candidate",
  "delivery_profile_ref": {
    "owner": "short-drama",
    "artifact": "short-drama.json",
    "hash": "<sha256>",
    "field": "/creator_authority/production_profile"
  },
  "members": [
    {
      "order": 1,
      "shot_ref": {
        "owner": "short-drama-storyboard",
        "artifact": "episodes/<EP>/storyboard/shots.jsonl",
        "hash": "<sha256>",
        "record_id": "SHOT-<id>"
      },
      "motion_ref": {
        "owner": "short-drama-video-prompts",
        "artifact": "episodes/<EP>/storyboard/motion-specs.jsonl",
        "hash": "<sha256>",
        "record_id": "MOTION-<stable-id>"
      },
      "accepted_duration_ref": {
        "owner": "short-drama-storyboard",
        "artifact": "episodes/<EP>/storyboard/shots.jsonl",
        "hash": "<sha256>",
        "record_id": "SHOT-<id>",
        "field": "/duration"
      },
      "accepted_duration": "<从 accepted_duration_ref 读到的值，投影不改写>"
    }
  ],
  "container_duration": "<各成员 accepted_duration 之和>",
  "membership_basis": {
    "source_order_contiguous": "<true | 说明为什么不连续及去向>",
    "binding_chain_ref": {
      "owner": "short-drama-storyboard",
      "artifact": "episodes/<EP>/storyboard/shots.jsonl",
      "hash": "<sha256>",
      "record_id": "SHOT-<id>",
      "field": "/bindings"
    },
    "scene_boundary_not_crossed": "<true | 说明跨越原因与已接受依据>"
  },
  "unresolved": [],
  "provenance": "creator_project"
}
```

## 结构校验点

`VID-13` 靠这条记录本地可证，不依赖阅读渲染文本：

1. `members[]` 非空，`order` 唯一、连续、升序；
2. 每个成员的 `accepted_duration` 等于其 `accepted_duration_ref` 指向的分镜值；
3. `container_duration` 等于各成员 `accepted_duration` 之和；
4. 每个成员的 `motion_ref` 指向的运动规格，其 `shot_ref` 与该成员 `shot_ref` 一致；
5. `membership_basis` 三项都有结论，未成立的写进 `unresolved`，不留空。

任何一项不成立即为结构缺陷，按主技能的 `stale` 与恢复流程处理，不在渲染文本里补救。

## 与其他记录的关系

- **运动规格**：每条运动规格仍然只绑定一个 `shot_ref`；被装进容器时增加 `container_ref`
  指回本记录。指针方向是 motion → container，不存在 container 改写 motion 的权限。
- **渲染文本**：`video-prompts.md` 的容器一节由本记录派生，是缓存，不是权威；文本与本
  记录不一致时以本记录为准。
- **成员时长**：一律是分镜的只读投影。要改时长就改分镜，然后重算 `container_duration`；
  不得在容器里直接改数。
- **成员资格判据**：语义部分见 `references/delivery-profile.md` 的多镜容器成员资格；
  本文件只负责让判据的结论可被引用与核对。

复制后删除不适用的可选字段。容器不跨越已接受的场次或时间跳跃；省略、闪回分支与声明过的
蒙太奇各自单独成容器。
