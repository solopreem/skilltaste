<div align="center">

# video-skills

[English](README.md) | [简体中文](README.zh-CN.md) | **日本語** | [한국어](README.ko.md) | [Español](README.es.md) | [Deutsch](README.de.md) | [Français](README.fr.md) | [Português](README.pt.md)

**センスのいい映像を、数分で作り直せます。**

</div>

```bash
npx skills add sonnyproto/video-skills                       # ライブラリ全体（エージェントがエントリを選ぶ）
npx skills add sonnyproto/video-skills/launch/broll-wheel   # この 1 本だけ
```

あとは Claude Code か Codex で：

```text
broll-wheel で https://your-product.com のローンチ映像を作って。
```

手動で入れるものはありません。エージェントがエントリの `scripts/setup.sh` を実行し、Node 20+、ffmpeg、Python 3 を確認して、
HyperFrames のスキルがなければインストールします。レンダラーは `npx` が固定バージョンで取得します。

## なぜ作ったか

いまの動画スキルは大きく 2 種類です。ひとつはクローズドなパッケージ：1 スタイルごとに購入、速いけれど中身は見えず、組み合わせもできない。
もうひとつは奥の深いオープンなツールキットで、それぞれ独自の形式なので互いに噛み合いません。

video-skills は前者のフラット版を、オープンに作ったものです：

- **1 エントリ = 1 本の映像。** それぞれ自分が生んだ `result.mp4` 付きなので、目で見て選べます。
- **再現可能。** 各エントリには映像をそのままレンダリングできる完全なプロジェクトと、ストック素材のソース ID、生成素材のプロンプトが入っています。API キーは不要です。
- **どこでも同じ形式。** 全エントリが同じファイル構成と同じ `taste.json` カードを持つので、比較でき、エージェントが組み合わせられます（[spec/ENTRY.md](spec/ENTRY.md)）。
- **プロダクトは 1 ファイルに。** 自分のプロダクトに差し替えるときは `film.json` と素材を編集するだけで、ジェネレーターには触りません。

## ライブラリ

<!-- CATALOG -->
| Preview | Entry | Category · method | Length | Events / 10 s |
|---|---|---|---|---|
| <img src="launch/broll-wheel/result/preview.gif" width="240"> | [**broll-wheel**](launch/broll-wheel/) B-roll wheel launch | launch · broll-under-type | 90 s 16:9 | 8.7 |
| <img src="launch/feature-roster/result/preview.gif" width="240"> | [**feature-roster**](launch/feature-roster/) Feature roster | launch · rebuilt-ui-roster | 26.7 s 16:9 + 9:16 | 3.0 |
<!-- /CATALOG -->

## エントリの構成

```
<category>/<id>/
├── SKILL.md       これを読み込んで映像を作る
├── taste.json     カード：依存関係、7 つのレイヤー、仕様、計測値、必要なもの、向いている用途
├── references/    floor.md（共通ルール）、sourcing.md（launch：本物の素材集め）、RECIPE.md（ショットごと）、SWAP.md（プロダクト差し替え）、REFERENCE.md
├── scripts/       setup.sh（足りないものを入れる）と計測スクリプト
├── result/        result.mp4、ポスター、コンタクトシート、プレビュー、metrics.json
└── project/       レンダリング可能なプロジェクト：film.json、tools/、assets/
```

すべてのエントリは同じ 7 つのレイヤーに位置づけられます：

| レイヤー | 問い |
|---|---|
| floor | 絶対に譲れないことは？（本物のプロダクトのみ、サンプルには表示、ブランド） |
| category | どんな種類の映像か？（ローンチ、解説、チュートリアル、データストーリー、SNS 用カット、ジングル） |
| method | 画をどう作り、骨格をどう流すか？（B ロール＋テキスト、カットしない 1 つの図形、ビートモンタージュ、3D UI…） |
| moves | 具体的にどんな手を入れるか？（ホイールの章区切り、マーカー線、アンカーモンタージュ、ピル変形…） |
| craft | 何が高級に見せるか？（3 秒でフック、35% 付近で盛り上げ、着地に効果音、-14 LUFS） |
| style | どう見えるか？（グレード、書体、配色の役割） |
| tool | 何でレンダリングするか？（HyperFrames、Remotion…） |

異なるレイヤー同士は衝突しません。同じレイヤー内では floor > category > method > moves > craft > style の順に優先します。

各エントリは自己完結しています。共通ファイル（floor ルール、計測スクリプト）は各エントリにコピーし、外部ツール
（HyperFrames、ffmpeg）は `taste.json` の `requires` で宣言するだけ。テイストは共有しません。詳しくは [spec/ENTRY.md](spec/ENTRY.md)。

## ツール

| | |
|---|---|
| `tools/floor.md` | 共通の floor ルール（各エントリの `references/` にコピー） |
| `launch/sourcing.md` | launch 用：プロダクトの本物の画面・ロゴ・コピーの集め方（各 launch エントリの `references/` にコピー） |
| `tools/validate.py` | 全エントリを形式に照らして検査し、共通ファイルのコピーが `tools/` と一致するか確認 |
| `tools/catalog.py` | `catalog.json` と上の表を再生成 |
| `tools/analyze.py <video> <out>` | カット、ショット、コンタクトシート、LUFS、トゥルーピーク、BPM、ビート上のカット |
| `tools/events.py <video> <out>` | 10 秒あたりの視覚変化イベント数と静止率 |

## 必要なもの

Node 20+、ffmpeg、Python 3。そのほかに必要なもの（レンダラーのバージョン、B ロール用の動画モデル、音楽モデル）は各エントリに書いてあります。

## コントリビュート

新しいエントリを歓迎します。[CONTRIBUTING.md](CONTRIBUTING.md) を参照してください。条件：プロジェクトがそのまま結果の映像をレンダリングできること、
プロダクトの内容が `film.json` にあること、結果が計測されていること、参考映像の素材を再配布しないこと。

## 謝辞

アイデアとルールを感謝とともに借りています：[HyperFrames](https://hyperframes.heygen.com)、
[huashu-motion](https://github.com/alchaincyf/huashu-motion)（リズムと演出ノート）、
[video-shotcraft](https://github.com/Vincentwei1021/video-shotcraft)（レシピカードと差し替えガイド）、
[product-launch-motion](https://github.com/AbubakrChan/product-launch-motion)（クラフトの細部）。

## ライセンス

broll-wheel の作例は、Meta のパーソナル AI エージェント Muse の非公式スペックフィルムです。Meta とは無関係で、
承認やスポンサーも受けていません。Muse とその素材は Meta のものであり、このリポジトリには含まれていません。

コード：MIT。結果の映像と生成素材：CC BY 4.0。作例のプロダクト素材は各所有者に帰属します。再利用できる範囲は各エントリの `taste.json` に記載しています。
