# RDE XPS用テンプレート

## 概要
XPSをご利用の方に適したテンプレートです。以下の装置メーカーに対応しています。
- DT0011: ULVAC-PHI
- DT0012: Scienta Omicron

XPSの専門家によって監修されたメタ情報を上記ファイルから自動的にRDEが抽出します。
- ULVAC-PHIの.spe/.pro/.angフォーマット、Scienta Omicronの.vmsフォーマットに対応したメタ情報の抽出、可視化を行う。
- MultiDataTile対応（１つの送り状で複数のデータ登録を行う）
- マジックネーム対応（データ名を${filename}とすると、ファイル名をデータ名にマッピングする）

## メタ情報
- [メタ情報](docs/requirement_analysis/要件定義.xlsx)

## 基本情報

### コンテナ情報
- 【コンテナ名】nims_mdpf_share_xps:v1.0

### テンプレート情報
- DT0011:
    - 【データセットテンプレートID】NIMS_DT0011_XPS_ULVAC-PHI_v1.0
    - 【データセットテンプレート名日本語】XPS ULVAC-PHI データセットテンプレート
    - 【データセットテンプレート名英語】XPS ULVAC-PHI dataset-template
    - 【データセットテンプレートの説明】ULVAC-PHIのXPSをご利用の方に適したモードです。spe/pro/angフォーマットでデータを取得されている方がご利用いただけます。 XPSの専門家によって監修されたメタ情報をspe/pro/angファイルから自動的にRDEが抽出します。 
    - 【バージョン】1.0
    - 【データセット種別】加工・計測レシピ型
    - 【データ構造化】あり (システム上「あり」を選択)
    - 【取り扱い事業】NIMS研究および共同研究プロジェクト (PROGRAM)
    - 【装置名】(なし。装置情報を紐づける場合はこのテンプレートを複製し、装置情報を設定すること。)
- DT0012:
    - 【データセットテンプレートID】NIMS_DT0012_XPS_ScientaOmicron_v1.0
    - 【データセットテンプレート名日本語】XPS Scienta Omicron データセットテンプレート
    - 【データセットテンプレート名英語】XPS Scienta Omicron dataset-template
    - 【データセットテンプレートの説明】Scienta OmicronのXPSをご利用の方に適したモードです。vmsフォーマットでデータを取得されている方がご利用いただけます。 XPSの専門家によって監修されたメタ情報をvmsファイルから自動的にRDEが抽出します。  
    - 【バージョン】1.0
    - 【データセット種別】加工・計測レシピ型
    - 【データ構造化】あり (システム上「あり」を選択)
    - 【取り扱い事業】NIMS研究および共同研究プロジェクト (PROGRAM)
    - 【装置名】(なし。装置情報を紐づける場合はこのテンプレートを複製し、装置情報を設定すること。)

### データ登録方法
- 送り状画面をひらいて入力ファイルに関する情報を入力する
- 「登録ファイル」欄に登録したいファイルをドラッグアンドドロップする。
  - 登録したいファイルのフォーマットは、\*.spe、\*.pro、\*.ang、\*.vms のどれか一つとなります。
  - 複数のファイルを入力し一度に複数のデータを登録することが可能。
  - 複数のファイルを入力する場合は、「データ名」に「${filename}」と入力し「データ名」に入力ファイル名をマッピングさせることができる
- 「登録開始」ボタンを押して（確認画面経由で）登録を開始する

## 構成

### レポジトリ構成

```
xps
├── LICENSE
├── README.md
├── container
│   ├── Dockerfile
│   ├── data (入出力(下記参照))
│   ├── main.py
│   ├── modules (ソースコード)
│   │   └── datasets_process.py (構造化処理の大元)
│   ├── modules_xps (ソースコード)
│   │   ├── factory.py (設定ファイル、使用クラス取得)
│   │   ├── graph_handler.py (グラフ描画)
│   │   ├── inputfile_handler.py (入力ファイル読み込み(共通部))
│   │   ├── interfaces.py
│   │   ├── invoice_handler.py (送り状上書き)
│   │   ├── meta_handler.py (メタデータ解析(共通部))
│   │   ├── models.py
│   │   ├── structured_handler.py (構造化データ解析(共通部))
│   │   ├── scienta-omicron (Scienta Omicron向け)
│   │   │   └── vms (vmsフォーマット用)
│   │   │       ├── graph_handler.py (グラフ描画)
│   │   │       ├── inputfile_handler.py (入力ファイル読み込み)
│   │   │       └── meta_handler.py (メタデータ解析)
│   │   └── ulvac-phi (ULVAC-PHI向け)
│   │       ├── structured_handler.py (構造化データ解析(ULVAC-PHI共通部))
│   │       ├── MPExport.exe (ULVAC-PHI製計測データデコードツール)
│   │       ├── pro (pro, angフォーマット用)
│   │       │   ├── inputfile_handler.py (入力ファイル読み込み)
│   │       │   └── meta_handler.py (メタデータ解析)
│   │       └── spe (speフォーマット用)
│   │           ├── inputfile_handler.py (入力ファイル読み込み)
│   │           └── meta_handler.py (メタデータ解析)
│   ├── pip.conf
│   ├── pyproject.toml
│   ├── requirements-test.txt
│   ├── requirements.txt
│   └── tox.ini
├── docs (ドキュメント)
│   ├── manual (マニュアル)
│   └── requirement_analysis (要件定義)
└── template (テンプレート群)
     ├── scienta-omicron (Scienta Omicron向け)
     │   ├── batch.yaml
     │   ├── catalog.schema.json (カタログ項目定義)
     │   ├── invoice.schema.json (送り状項目定義)
     │   ├── jobs.template.yaml
     │   ├── metadata-def.json (メタデータ定義(RDE画面表示用))
     │   └── tasksupport
     │        ├── default_value.csv (初期値設定)
     │        ├── invoice.schema.json (送り状項目定義)
     │        ├── metadata-def.json (メタデータ定義)
     │        └── rdeconfig.yaml (設定ファイル)
     └─ ulvac-phi (ULVAC-PHI向け)
         ├── batch.yaml
         ├── catalog.schema.json (カタログ項目定義)
         ├── invoice.schema.json (送り状項目定義)
         ├── jobs.template.yaml
         ├── metadata-def.json (メタデータ定義(RDE画面表示用))
         └── tasksupport
             ├── default_value.csv (初期値設定)
             ├── invoice.schema.json (送り状項目定義)
             ├── metadata-def.json (メタデータ定義)
             └── rdeconfig.yaml (設定ファイル)

```

### 動作環境ファイル入出力

```
│   ├── container/data
│   │   ├── attachment
│   │   ├── inputdata
│   │   │   └── 登録ファイル欄にドラッグアンドドロップした任意のファイル
│   │   ├── invoice
│   │   │   └── invoice.json (送り状ファイル)
│   │   ├── main_image
│   │   │   └── (メイン)プロット画像
│   │   ├── meta
│   │   │   └── metadata.json (主要パラメータメタ情報ファイル)
│   │   ├── nonshared_raw
│   │   │   └── inputdataからコピーした入力ファイル
│   │   ├── other_image
│   │   │   └── (メイン以外の)プロット画像
│   │   ├── structured
│   │   │   ├── *.txt (前処理した計測データ)
│   │   │   └── *.csv (スペクトルデータ)
│   │   ├── tasksupport (テンプレート群)
│   │   │   ├── default_value.csv
│   │   │   ├── invoice.schema.json
│   │   │   ├── metadata-def.json
│   │   │   └── rdeconfig.yaml
│   │   └── thumbnail
│   │       └── (サムネイル用)プロット画像
```

## データ閲覧
- データ一覧画面を開く。
- ギャラリー表示タブでは１データがタイル状に並べられている。データ名をクリックして詳細を閲覧する。
- ツリー表示タブではタクソノミーにしたがってデータを階層表示する。データ名をクリックして詳細を閲覧する。

### 動作環境
- Python: 3.11
- RDEToolKit: 1.2.0

## 入力ファイルから抽出するメタデータを追加(変更)する場合
- 入力ファイルから抽出するメタデータを追加(変更)する場合、以下のファイルを修正する必要があります。
    - metadata-def.json ('ULVAC-PHI'用と'Scienta Omicron'用が別れているので、注意。)
<br>

- 上記ファイルに、以下のようにオブジェクトを追加(変更)する必要があります。
```
    },
    "spe.voltage_unit": {    ← metadata.json(出力ファイル)に記述したい名称 (重複不可)
        "name": {
            "ja": "電圧単位",    ← RDEのデータ詳細画面の'日本語名'に表示したい名称
            "en": "Voltage unit"    ← RDEのデータ詳細画面の'英語名'に表示したい名称
        },
        "schema": {
            "type": "string"　← 計測ファイルに書かれているメタデータ項目の値のデータ型 (文字列: "string", 数字: "number")
        },
        "order": 31,　← metadata.json(出力ファイル)上での記述順番 (重複不可、記述順を気にしない場合、この行自体不要)
        "unit": "kV" ← 単位(単位を出力しない場合、この行自体不要)
        "originalName": "HW_XG_VOLTAGE_UNIT",　← 計測ファイルに書かれているメタデータ項目 (重複不可、計測ファイルの項目を元にしない場合、この行自体不要)
        "variable": 1　← 0:固定長項目 1:可変長項目(複数ブロック・複数元素向け)
    },
    "spe.***": {
```
