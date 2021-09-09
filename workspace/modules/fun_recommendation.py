import numpy as np
import pandas as pd

# ガウス過程回帰
import GPy

# 多重対応分析の結果のcsvの保存場所
FUN_FEATURES = '/home/workspace/data/fun_features.csv'


def run(y_json):
    fun_features = pd.read_csv(FUN_FEATURES, index_col=0)
    df_y = _json2dataframe(y_json)
    x_train, y_train = _create_train_set(fun_features, df_y)
    y_pred = _calc_gpr(fun_features, x_train, y_train)
    return to_json(y_pred["95%"])
    
    
def _json2dataframe(y_json):
    for i, one_json in enumerate(y_json):
        shaping_json = {"{}".format(i): one_json} 
        input_json = str(shaping_json).replace("'", '"')
        se_y = pd.read_json(input_json) # json to Series
        # 初回だけdfにseを代入し，2回目以降はdfとseを結合する
        df_y = se_y if i == 0 else pd.concat([df_y, se_y], axis=1)
    df_y  = df_y.reindex(index=y_json[0].keys()) # indexの順番をjsonと同じにする
    df_y.drop(['id'], inplace=True)
    return df_y.T


def _create_train_set(fun_features, df_y):
    x_train = fun_features.loc[df_y['hangout_id']]
    y_train = pd.DataFrame(df_y['fun_score'])
    return x_train, y_train


def _calc_gpr(fun_features, x_train, y_train):
    dim = len(x_train.columns)
    #kernel = GPy.kern.Matern32(dim) + GPy.kern.Linear(dim) + GPy.kern.Bias(dim) + GPy.kern.White(dim)
    kernel = GPy.kern.RBF(dim) + GPy.kern.Linear(dim) + GPy.kern.Bias(dim) + GPy.kern.White(dim)
    # モデルの学習
    model = GPy.models.GPRegression(x_train, y_train, kernel)
    model.optimize()
    # 予測結果
    y_qua_pred = model.predict_quantiles(fun_features.values, quantiles=(5, 50, 95))
    y_pred = pd.DataFrame(np.array(y_qua_pred).reshape(3,len(y_qua_pred[0])).T)
    y_pred.index = fun_features.index
    y_pred.columns = ["5%","expected value","95%"]
    return y_pred

    
def to_json(y_pred):
    y_pred_json = []
    for i, val in enumerate(y_pred):
        y_pred_json.append(dict(id=i, val=val))
    return y_pred_json