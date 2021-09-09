import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import japanize_matplotlib

# 多重対応分析
import mca

# 遊び特徴量の出力先
OUTPUT_LOCATION = '/home/workspace/data/'
OUTPUT_FILENAME = 'fun_features.csv'

def run(json, visualization=False):
    playlist = _data_processing(json)
    fun_features = _calc_mca(playlist, visualization)
    # CSVへ書き出す
    fun_features.to_csv(OUTPUT_LOCATION+OUTPUT_FILENAME, index=False)

def _data_processing(json):
    df_json = _json2dataframe(json)
    dp_json = _data_cleansing(df_json)
    return dp_json
    
def _json2dataframe(json):
    for i, one_json in enumerate(json):
        shaping_json = {'calumns': one_json} 
        input_json = str(shaping_json).replace("'", '"')
        se_json = pd.read_json(input_json) # json to Series
        # 初回だけdfにseを代入し，2回目以降はdfとseを結合する
        df_json = se_json if i == 0 else pd.concat([df_json, se_json], axis=1)
    df_json  = df_json.reindex(index=json[0].keys()) # indexの順番をjsonと同じにする
    return df_json

def _data_cleansing(df_json):
    df_json.columns = df_json.loc['id'] # カラム名を遊びIDに変更
    df_json.drop(['created_at','updated_at','name','id'], inplace=True) # いらん情報を削除
    df_json = df_json.T # 転置
    return df_json

def _calc_mca(playlist, visualization):
    mca_counts = mca.MCA(playlist.astype(float)) # 値がfloatじゃないとエラー出る
    # 結果データ抜き出し
    # 2次元表示のためN=2とする
    rows = mca_counts.fs_r(N=2)  # 表側データ
    cols = mca_counts.fs_c(N=2)  # 表頭データ
    if visualization == True:
        _visualize(playlist, rows, cols)
    return pd.DataFrame(rows).set_index(playlist.index)

# 結果の可視化
def _visualize(playlist, rows, cols):
    fig = plt.figure()
    # 表側
    plt.scatter(rows[:, 0], rows[:, 1], c='b', marker="None")
    labels = playlist.index
    for label, x, y in zip(labels, rows[:, 0], rows[:, 1]):
        plt.annotate(label, xy=(x, y), c="b")
    # 表頭
    plt.scatter(cols[:, 0], cols[:, 1], c='r', marker="None")
    labels = playlist.columns
    for label, x, y in zip(labels, cols[:, 0], cols[:, 1]):
        plt.annotate(label, xy=(x, y), c="r")
    # xy軸
    plt.axhline(0, color='gray')
    plt.axvline(0, color='gray')
    
    fig.savefig(OUTPUT_LOCATION+'visualization.png')