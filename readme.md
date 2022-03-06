# 概要

webカメラから画像を取得し、Azureの特定のBlob Storageにアップロードするサンプル.

## 使い方

1. pipenvを使用してパッケージのインストール
`pipenv sync`

2. config.iniを作成して、その中にAzure Blob Containerの接続文字列を記載

3. pipenv run startで撮影&アップロード
