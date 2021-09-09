# 遊び&友人候補レコメンドモデル
多重対応分析とガウス過程回帰による推薦モデルの構築

## 遊びレコメンドモデル
1. 色々な遊びに対し，主観が(限りなく)含まれない大量(目標は100項目前後)の質問を取ることで，遊びの情報を獲得する
1. スパース空間であり，カテゴリ変数でもあるため，多重対応分析(Multiple Correspondence Analysis; MCA)を用いることで次元削減を行い，これらを『遊び特徴量』とする
1. ユーザーにいくつかの遊びを提示し，それらの頻度を回答してもらうことで，ある遊びの『遊び特徴量』を入力した際の満足度を予測するためのモデルを構築する
1. サンプル数が少ないと考えられるため，ガウス過程回帰によってあるユーザーの満足度分布の近似分布を算出し，それをもとに遊びレコメンドを試みる

## 友人候補レコメンドモデル
1. 遊びレコメンドモデルから遊び満足度近似分布が求められるので，ユーザ間の近似分布の相関を取ることで，友人候補をレコメンドする
1. 発展では，区間推定をうまいこと使いたいなーって考えてるよ

# 参考文献
- [Multiple correspondence analysis](https://github.com/esafak/mca)
- [Pythonでコレスポンデンス分析をやってみた](https://lab.astamuse.co.jp/entry/Python-analytics-Correspondence_)
- [多変量解析メモ: 多重対応分析(Multiple Correspondence Analysis, MCA)](https://qiita.com/m1t0/items/36418142853acc808813) → アルゴリズムの解説
- [コレスポンデンス分析のやり方を解説【Python】](https://self-development.info/%E3%82%B3%E3%83%AC%E3%82%B9%E3%83%9D%E3%83%B3%E3%83%87%E3%83%B3%E3%82%B9%E5%88%86%E6%9E%90%E3%81%AE%E3%82%84%E3%82%8A%E6%96%B9%E3%82%92%E8%A7%A3%E8%AA%AC%E3%80%90python%E3%80%91/) → 実装の解説
- [多重対応分析](https://www.amazon.co.jp/%E5%A4%9A%E9%87%8D%E5%AF%BE%E5%BF%9C%E5%88%86%E6%9E%90-Brigitte-Roux/dp/4274226050/ref=sr_1_1?__mk_ja_JP=%E3%82%AB%E3%82%BF%E3%82%AB%E3%83%8A&dchild=1&keywords=%E5%A4%9A%E9%87%8D%E5%AF%BE%E5%BF%9C%E5%88%86%E6%9E%90&qid=1631173791&sr=8-1) → 読んだ本
