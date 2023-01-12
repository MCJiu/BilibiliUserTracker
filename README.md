![TopImage](https://s2.loli.net/2023/01/12/ExCVD5NTQ21WaBv.png)

# Bilibili User  Tracker

## 简介

这是一个简单的爬取Bilibili用户数据的网络爬虫

## 用法

### 环境要求

- Python 3.11.1
- Python packages:
  1. loguru
  2. numpy
  3. pymongo
- MongoDB 6

### 配置参数

配置MongoDB主机和端口

配置cookie（可选）

配置代理（可选）

**警告**：虽然配置cookie是可选的，但不配置cookie时，请求API容易返回-401状态码，即非法访问

### 执行脚本

```shell
$ python .\scripts\update_data.py
```

## 其他说明

- Bilibili的API会返回很多数据，代码中仅选取了少量作为测试，可以参考 [Bilibili API 文档（非官方）](https://github.com/SocialSisterYi/bilibili-API-collect)查看完整数据



