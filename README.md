# 历史天气可视化

![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/Weather-v1.0-informational.svg)  ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/vue-v3.2.26-green.svg) ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/element--plus-v1.3.0-orange.svg)  ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/Flask-v2.0.2-green.svg) ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/liscense.svg)

这是一个可视化中国各地区历年（2011年~）历史天气状况的项目，基本涵盖中国绝大部分地区（包括港澳台及钓鱼岛等地区）。这个项目由笔者之前科研过程中的小成果衍生而来。因之前研究需要用到历史天气数据，因此笔者专门写了个爬虫爬取`http://tianqi.2345.com` 这个网站的历史天气数据。一方面是为了做个小项目练练手，一方面也是为了方便其他有需要的童鞋，笔者花了一周的时间将其做成了web系统，前后端分离开发。为了方便使用，笔者将其做成了docker镜像并上传到了阿里云，用户只需要两条命令即可运行。

## 使用方式

+ ```shell
  docker pull registry.cn-hangzhou.aliyuncs.com/lymboy/weather:1.0
  ```

+ ```shell
  docker run -p 8000:8000 -d registry.cn-hangzhou.aliyuncs.com/lymboy/weather:1.0
  ```

![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/image-20220109223034013.png)

## 代码开发

![系统架构](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/architecture.png)

本项目采用前后端分离开发。前端使用Vue3，Element Plus，Echarts和Axios。后端使用Python3和Flash框架，天气数据爬取自`http://tianqi.2345.com`。

### 运行前端

前端项目使用的构建工具是`yarn`需要提前安装。

```shell
git clone https://github.com/lymboy/Weather.git
cd Weather/Vue-UI/
yarn install
yarn run serve
```

### 运行后端

```shell
cd Server/
pip install --ignore-installed -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
python3 main.py		# 主入口文件，main函数
```

<img src="https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/image-20220109215546382.png" style="zoom: 60%;" /> <img src="https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/image-20220109215435316.png" style="zoom:60%;" /> 

### 部署方式

前后端分离便于解耦和简化开发，部署时仍可以集成部署。具体步骤为：

+ 将前端项目编译，会生成`dist`目录，里面是编译好的文件`index.html`，`favicon.ico`，`static`
+ 将编译好的前端文件放到后端对应的目录下。`index.html`放到`templates`目录，`favicon.ico`移到`static`文件夹内拷贝到后端项目文件夹内

> 因`favicon.ico`位置有变动，需要修改`templates/index.html`对应内容
>
> ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/image-20220109222505750.png)

`Flask`官方指出`Flask run`的方式不适合生产环境，这里使用`gunicorn`服务器来运行项目，在后端项目根路径下执行

```shell
gunicorn -w 4 -b 0.0.0.0:8000 main:app
```

### 镜像构建

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

## 不足与改进之处

+ 页面加载比较缓慢

  因为项目的DAO层（概念取自Java web）是通过爬虫爬取相关网站的数据解析后再返回给前端渲染，因此速度会比较慢，如果查询的数据比较多，如查询10年的数据可能会超时失败（默认超时时间10s）。一个改进策略是将爬取过的数据存到数据库中，前端发出的所有数据查询请求都从数据库中查询，如果数据库中不存在再爬取相关数据存入到数据库。或者事先将所有数据全部存入数据库，也可以引入`redis`等缓存数据库等。

  这样应该可以显著优化，不过笔者太忙了，有兴趣的读者可以自行尝试下，今后有空会试着实现下。过去10年（2011-2021）的数据之前笔者已经爬取下来了，有兴趣的读者可以联系alayama@163.com。

![架构改进](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/architecture-advance.png)

+ 功能比较欠缺

  事实上这是笔者闲时玩的一个小项目，没有考虑很多具体需求，因此界面比较单调，功能也比较欠缺。有兴趣的读者可以和我交流或者自行开发和改进。

  可以考虑结合百度地图显示全国范围内的气温热力图，空气质量热力图等，类似下面酱紫↓

  ![](https://itbird.oss-cn-beijing.aliyuncs.com/img-md/2022/01/09/image-20220109231110744.png)

+ 数据下载

  有些研究同学可能需要相关数据做研究，可以考虑在前端添加下载按钮让用户可以选择下载特定地区特定时间的数据，数据格式可以是`Excel`，`CSV`等。

……



