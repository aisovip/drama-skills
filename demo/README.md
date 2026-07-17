# Demo：一集短剧的全链路产出

本目录展示套件从剧本到视频提示词的完整文本链路。题材为都市打脸（合成示例，
情节、人物、地名均为原创虚构；工艺规则来自 skills 各 reference）。

| 文件 | 环节 | 对应 skill |
|---|---|---|
| [EP001-剧本.md](EP001-剧本.md) | 分集剧本（生产方言格式） | `short-drama-write` |
| [EP001-资产设定.md](EP001-资产设定.md) | 角色三视图 / 场景方位图 / 物品白底图 | `short-drama-assets` + `short-drama-image-prompts` |
| [EP001-分镜.md](EP001-分镜.md) | 拍→镜翻译 + 五连接词时序链 | `short-drama-storyboard` |
| [EP001-视频提示词.md](EP001-视频提示词.md) | 15s 分镜组成片提示词 | `short-drama-video-prompts` |

阅读顺序即生产顺序。可对照各文件开头的"工艺要点"回看对应 reference 的规则。
