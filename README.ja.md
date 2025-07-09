# AlphaGenome Docker 環境

このDockerイメージは、[AlphaGenome](https://github.com/google-deepmind/alphagenome?tab=readme-ov-file)および一般的なデータサイエンス向けライブラリがインストールされた、最小限のPython環境を提供します。Google Colabに近い環境をローカルやオフラインで再現することを目的としています。

## 含まれるライブラリ

- alphagenome
- matplotlib
- pandas

## 必要条件

- Dockerのインストール（https://docs.docker.com/get-docker/ を参照）

## イメージのビルド

Dockerイメージをビルドするには、以下を実行します：

```bash
docker build -t alphagenome-env .
```

これにより、`alphagenome-env` という名前のイメージが作成されます。

## 対話型Pythonセッションの実行

コンテナ内で対話型のPythonセッションを開始するには：

```bash
docker run -it --rm alphagenome-env
```

## AlphaGenome APIキーの使用

APIキーを使って `run.py` を実行するには、環境変数として渡すことができます：

```bash
docker run -it --rm \
  -v $(pwd):/alphagenome \
  -e API_KEY=your_real_api_key_here \
  alphagenome-env python run.py
```

もしくは、このディレクトリに以下の内容を含む `.env` ファイルを作成してください：

```ini
API_KEY=your_real_api_key_here
```

その後、次のコマンドでコンテナを実行します：

```bash
docker run -it --rm \
  -v $(pwd):/alphagenome \
  --env-file .env \
  alphagenome-env python run.py
```

## 作業ディレクトリのカスタマイズ

デフォルトでは、コンテナ内の作業ディレクトリは `/alphagenome` に設定されています。

ローカルのプロジェクトディレクトリをこれにマウントするには：

```bash
docker run -it --rm -v $(pwd):/alphagenome alphagenome-env
```

## AlphaGenomeで利用できる解析

| 出力種別              | 説明　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　                 | 対象とするデータ・解釈                                               |
|------------------------|--------------------------------------------------------------------------------|---------------------------------------------------------------------|
| ATAC                   | Tn5トランスポザーゼを用いてクロマチンの開いた領域を検出                          | オープンクロマチン領域、調節活性の指標                              |
| CAGE                   | 5’キャップ化RNAを基に転写開始点（TSS）を特定                                     | プロモーター活性、正確なTSSの位置                                   |
| DNASE                  | DNase I感受性部位（DHS）を検出                                                  | エンハンサーやプロモーターなどの制御領域                             |
| RNA_SEQ                | RNAシーケンスによる遺伝子発現量の定量                                           | 発現量の推定、スプライシングパターンの解析                          |
| CHIP_HISTONE           | ヒストン修飾（例：H3K27acなど）に対するChIP-seq解析                             | 活性なエピジェネティックマーク、クロマチン状態の評価                |
| CHIP_TF                | 転写因子に対するChIP-seq解析                                                    | TF結合部位の特定、調節ネットワークの構築                            |
| SPLICE_SITES           | スプライスドナー／アクセプター部位の注釈または予測                             | エクソン-イントロン境界、スプライスシグナル                          |
| SPLICE_SITE_USAGE      | 各スプライス部位の使用頻度などの定量的情報                                     | スプライシングの動態、アイソフォームの切り替えの解析                |
| SPLICE_JUNCTIONS       | RNA-seqリードから推定されるエクソン接合部                                        | 代替スプライシングの検出                                            |
| CONTACT_MAPS           | Hi-CやMicro-Cなどによるクロマチン相互作用データ                                 | 3次元ゲノム構造、エンハンサー・プロモーターのループ解析             |
| PROCAP                 | 精密なrun-on法による転写開始点の高解像度検出                                   | 活性なTSSの検出、エンハンサーの転写活性評価                         |


## オプション：JupyterLabの使用

Pythonシェルの代わりにJupyterLabを起動するには、Dockerfile内のCMDを変更するか、以下のように上書きします：

```bash
docker run -it --rm -p 8888:8888 alphagenome-env jupyter lab --ip=0.0.0.0 --allow-root --no-browser
```

その後、ブラウザで http://localhost:8888 にアクセスしてください。

## ライセンス

このプロジェクトはMITライセンスの下で提供されています。詳細は LICENSE ファイルをご覧ください。
