# 课题四 后端框架

2021.5

## 1 Background

按照吴老师要求的划分，该框架总共需有 4 个功能：

1. 数据请求与数据筛选，以及数据分发；
2. 部署异常检测模型；
3. 异常检测模型发现异常事件后，制定 unity 上显示异常区域的策略；
4. 发现异常后，制定异常响应策略；

除上述四个功能外，该框架还需要作为 web 服务器端，为 unity 客户端和网页客户端的各种数据请求提供响应。



这次编写代码的基本原则是：以实现基本功能为目标，降低实现的时间成本；基本写法是：将所有任务放在一个进程中执行，数据的传递通过函数传参进行。这个写法的好处是：1. 避免多进程之间的通信开支；2. 代码复杂度低。

依据上述基本原则，将项目目录划分如下：

- /framework 包含吴老师所需的 4 个功能
  - /config 在 config 中，可以注释掉不需要的模型配置和数据配置，以降低调试难度
  - /request
  - /data_preprocess
  - /model_deploy
  - /anomaly_response_strategy
- /models 包含所有需要部署的异常检测模型
  - /fire_classification
  - /MNAD
  - /PVCGN
  - /weather_classification
  - /crowd_count
- flask_server.py 作为 web 服务器的主程序

### (废弃)原定架构

前端作为 1. 数据请求客户端；2. 数据分发客户端

后端作为 http 服务器 接收前端的数据和请求，进行 1. 模型部署 2. 异常应对策略 3. 异常传感器显示策略

[深度学习模型最佳部署方式：用Python实现HTTP服务器作API接口](https://blog.ailemon.me/2020/11/09/dl-best-deployment-python-impl-http-api-server/)



## 2 install

模型部署相关：

1. pytorch

2. timm

3. pytorch-geometric (徐博的 OD 预测依赖于 pytorch-geometric)

   https://pytorch-geometric.readthedocs.io/en/latest/notes/installation.html

web 服务器相关：

1. flask
2. flask-apscheduler



## 3 To do

- functions to add:

  1. 修改 gen_frame 等三个函数传递视频异常检测图片流的做法，直接传递 gif 图像给前端（目前已在 create_frame 等三个函数中实现保存 gif 图像到本地）

     这有两种做法：

     - 做法 1： 在保存 gif 图像到本地之后，在传输前重新读取 gif 图像到内存
     - 做法 2： 不将 gif 图像保存到本地，二是将 gif 图像直接保存到内存中的 BytesIO 对象

  2. 设置 pytorch 使用的 gpus（目前在 flask_server.py 中尝试加入 os.environ['gpus'] = '1,3' ，无效）

- Bugs to fix:

  1. 在使用 flask-apscheduler 时遇到问题： skipped: maximum number of running instances reached (1)

     [flask扩展插件---flask_apscheduler 定时任务框架](https://zhuanlan.zhihu.com/p/359302849)

     大约在 flask_server.py 中的 one_step 执行到两百多步后频繁出现。