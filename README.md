# 历史天气可视化

![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/Weather-v1.0-informational.svg)  ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/vue-v3.2.26-green.svg) ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/element--plus-v1.3.0-orange.svg)  ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/Flask-v2.0.2-green.svg) ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/liscense.svg)

本项目由笔者之前科研过程中的小成果衍生而来。因之前研究需要用到历史天气数据，因此笔者专门写了个爬虫爬取`http://tianqi.2345.com` 这个网站的历史天气数据。一方面是为了做个小项目练练手，一方面也是为了方便其他童鞋，笔者花了一周的时间将其做成了web系统，前后端分离开发。为了方便使用，笔者将其做成了docker镜像并上传到了阿里云，用户只需要两条命令即可运行。

## 使用方式

+ ```shell
  docker pull registry.cn-hangzhou.aliyuncs.com/lymboy/weather:1.0
  ```

+ ```shell
  docker run -p 8000:8000 -d registry.cn-hangzhou.aliyuncs.com/lymboy/weather:1.0
  ```

## 镜像构建

本项目docker镜像基于`conda/miniconda3`镜像构建，但是容器在`pip`安装依赖是出现各种问题，笔者修复这些问题后基于重新构建了新镜像并上传到阿里云，地址：`egistry.cn-hangzhou.aliyuncs.com/lymboy/full_conda3:1.0`，除此之外未做任何修改，有需要的读者可放心使用。

本项目的Dockerfile如下所示：

```dockerfile
FROM registry.cn-hangzhou.aliyuncs.com/lymboy/full_conda3:1.0

COPY Server /opt/Weather/Server
WORKDIR /opt/Weather/Server

RUN pip install --ignore-installed -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

EXPOSE 8000
CMD [ "gunicorn", "-b", "0.0.0.0:8000", "main:app" ]
```

> 原`conda/miniconda3`容器缺少相关依赖，可用以下命令修复
>
> ```shell
> apt install openssl gcc g++ libssl-dev libblas3 liblapack3 liblapack-dev libblas-dev gfortran libatlas-base-dev Pillow libjpeg-dev zlib1g-dev -y
> python3 -m pip install --upgrade Pillow
> ```

## 代码开发

![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/历史天气系统架构.png)

本项目采用前后端分离开发。前端使用Vue3，Element Plus，Echarts和Axios。后端使用Python3和Flash框架，天气数据爬取自`http://tianqi.2345.com`。







