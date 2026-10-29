<div align="center">

# video-skills

[English](README.md) | **简体中文** | [日本語](README.ja.md) | [한국어](README.ko.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Português](README.pt.md)

**一支支做好的视频，你的 AI 能照着给你的产品重做一支。**

挑一支喜欢的，告诉 agent 你的产品，就得到同样的片子。

几分钟给你的产品重做一支好片，品味自带。

</div>

```bash
npx skills add sonnyproto/video-skills                       # 整个库（agent 帮你挑条目）
npx skills add sonnyproto/video-skills/launch/broll-wheel   # 只要这一支
```

然后在 Claude Code 或 Codex 里说：

```text
用 broll-wheel 给 https://your-product.com 做一支发布片。
```

不用手动装别的：agent 会自己运行条目里的 `scripts/setup.sh`，检查 Node 20+、ffmpeg 和 Python 3，缺 HyperFrames skill 就自动装上。渲染器由 `npx` 按固定版本自动下载。

## 为什么做这个

现在的视频 skill 大致两种。一种是闭源整包：一个风格一个价，快，但看不到里面，也没法混用。另一种是很深的开源工具箱，各自一套格式，彼此对不上。

video-skills 是前一种的开源平铺版：

- **一个条目就是一支片。** 每条都带着它做出来的 `result.mp4`，用眼睛挑。
- **可复现。** 每条都带完整工程，原样渲染就得到那支片；实拍素材附来源 ID，生成类素材附提示词，不需要任何 API key。
- **格式完全一致。** 每条文件相同、`taste.json` 卡片相同，可以横向比较，agent 也能组合（见 [spec/ENTRY.md](spec/ENTRY.md)）。
- **产品集中在一个文件。** 换产品只改 `film.json` 和素材，不改生成器。

## 片库

<!-- CATALOG -->
| Preview | Entry | Category · method | Length | Events / 10 s |
|---|---|---|---|---|
| <img src="launch/broll-wheel/result/preview.gif" width="240"> | [**broll-wheel**](launch/broll-wheel/) B-roll wheel launch | launch · broll-under-type | 90 s 16:9 | 8.7 |
| <img src="launch/feature-roster/result/preview.gif" width="240"> | [**feature-roster**](launch/feature-roster/) Feature roster | launch · rebuilt-ui-roster | 26.7 s 16:9 + 9:16 | 3.0 |
<!-- /CATALOG -->

## 一个条目长什么样

```
<category>/<id>/
├── SKILL.md       加载它就能做片
├── taste.json     卡片：依赖、七层归属、规格、实测数据、需要什么、适合什么
├── references/    floor.md（共享底线）、sourcing.md（launch：找真实素材）、RECIPE.md（逐镜头配方）、SWAP.md（换产品）、REFERENCE.md（参考拆解）
├── scripts/       setup.sh（缺什么装什么）和测量脚本
├── result/        成片、封面、联系表、预览、metrics.json
└── project/       可直接渲染的工程：film.json、tools/、assets/
```

每个条目都按同样七层归档：

| 层 | 回答什么 |
|---|---|
| 底线 floor | 什么不能商量（只用真实产品、示意内容要标注、客户品牌） |
| 品类 category | 拍什么片（发布片、讲解、教程、数据故事、社媒短切、片头） |
| 做法 method | 画面怎么做、主干怎么走（实拍加字卡、单形状不切、卡拍快切、3D 界面……） |
| 招式 moves | 填进去的具体镜头（转轮分章、荧光笔划线、锚点快切、胶囊变形……） |
| 手艺 craft | 怎么做得高级（3 秒内钩子、35% 附近爆发、落点有音效、-14 LUFS） |
| 风格 style | 长什么样（调色、字体、配色角色） |
| 工具 tool | 用什么渲染（HyperFrames、Remotion……） |

不同层之间不冲突；同层冲突时：底线 > 品类 > 做法 > 招式 > 手艺 > 风格。

每个条目完全自足：我们自己的共享文件（底线、测量脚本）复制进每个条目；外部工具（HyperFrames、ffmpeg）只在 `taste.json` 的 `requires` 里声明；审美规则从不共享。详见 [spec/ENTRY.md](spec/ENTRY.md)。

## 工具

| | |
|---|---|
| `tools/floor.md` | 共享底线规则（复制进每个条目的 `references/`） |
| `launch/sourcing.md` | launch 赛道的素材规则：怎么找产品真实的截图、logo 和文案（复制进每个 launch 条目的 `references/`） |
| `tools/validate.py` | 按格式检查每个条目，并确认条目里的共享文件副本和 `tools/` 一致 |
| `tools/catalog.py` | 重建 `catalog.json` 和上面的片库表 |
| `tools/analyze.py <video> <out>` | 剪辑点、镜头、联系表、LUFS、真峰值、BPM、卡拍比例 |
| `tools/events.py <video> <out>` | 每 10 秒的画面变化事件数和静止占比 |

## 要求

Node 20+、ffmpeg、Python 3。条目会写明还需要什么（渲染器版本、生成空镜的视频模型、音乐模型）。

## 贡献

欢迎提交新条目，见 [CONTRIBUTING.md](CONTRIBUTING.md)。门槛：工程原样渲染出它的成片，产品内容都在 `film.json` 里，成片有实测数据，参考片的任何内容都不再分发。

## 致谢

以下项目的想法和规则给了我们很多帮助：[HyperFrames](https://hyperframes.heygen.com)、
[huashu-motion](https://github.com/alchaincyf/huashu-motion)（节奏和导演笔记）、
[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)（配方卡和换产品指南）、
[product-launch-motion](https://github.com/AbubakrChan/product-launch-motion)（手艺细节）。

## 许可

broll-wheel 的示例片是给 Meta 的个人 AI agent Muse 做的非官方提案片，与 Meta 无关，未获其认可或赞助；Muse 及其素材归 Meta 所有，不在本仓库中。

代码：MIT。成片和生成素材：CC BY 4.0。示例产品素材归各自所有者；每个条目的 `taste.json` 写明哪些可以复用。
