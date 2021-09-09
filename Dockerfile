FROM python:3.7

RUN apt update && apt -y upgrade

# 以下はjupyterlabの拡張機能を使うための前処理(最新版のnode.jpのインストール)
RUN apt install -y nodejs npm curl
RUN npm install n -g
RUN n stable
RUN ln -sf /usr/local/bin/node /usr/bin/node
RUN apt purge -y nodejs npm

# pythonのライブラリ
WORKDIR /home
COPY requirements.txt ${PWD}
RUN python3.7 -m pip install -r requirements.txt
# 多重対応分析
RUN python3.7 -m pip install --user mca

## JupyterLabの拡張機能
# jupyterlabの"Table of Contents"
RUN jupyter labextension install @jupyterlab/toc


# 作業ディレクトリ
WORKDIR /home/workspace