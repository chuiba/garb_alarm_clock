================
garb-alarm-clock
================

B 站装扮编号小闹钟，用于定时刷新并展示指定装扮信息（名称、粉丝编号、头像以及剩余库存）。项目最初开发于 2021 年，目前已经针对最新的 B 站接口做了兼容性调整。

.. contents:: 目录
   :local:
   :depth: 2

项目亮点
========

* 通过非官方接口实时获取 B 站装扮信息，自动绕过 412 限流。
* 图形界面基于 PyQt5，展示装扮名称、粉丝编号、更新时间及装扮背景。
* 支持自定义刷新间隔，默认限制为一分钟，以避免被接口限流。

运行环境
========

* Python 3.9+
* 依赖库：``PyQt5``、``requests``
* 推荐在 Windows 环境下运行（原始项目即针对 Windows 打包），其它桌面平台可自行测试。

快速开始
========

1. 克隆项目仓库并进入目录：

   .. code-block:: console

      git clone https://github.com/chuiba/garb_alarm_clock.git
      cd garb_alarm_clock

2. 创建虚拟环境并安装依赖：

   .. code-block:: console

      python -m venv .venv
      .venv\\Scripts\\activate
      pip install PyQt5 requests

3. 启动小闹钟：

   .. code-block:: console

      python -m garb_alarm_clock

   或者在 IDE 中运行 ``garb_alarm_clock/__init__.py`` 文件。

使用说明
========

* ``提醒编号``：输入要监控的粉丝卡提醒 ID。
* ``装扮编号``：输入装扮的 ``item_id``，点击 ``开启`` 后即可加载对应数据。
* ``刷新间隔``：单位为秒。小于 60 秒时会被自动重置为 60 秒，以防止频繁请求。
* 计时器归零时会自动重新请求接口并更新界面背景、头像和粉丝编号。

接口兼容性
==========

B 站在 2023 年之后对装扮接口增加了浏览器校验。本项目已经在 ``garb.py`` 中补充了浏览器标识头，如需二次开发请保留 ``User-Agent``、``Origin``、``Referer`` 这些请求头。若出现 412 错误，可尝试：

* 确认本地网络未拦截 ``https://api.bilibili.com``
* 调整刷新间隔，避免短时间内请求过多
* 在请求头中加入当前常用浏览器的 User-Agent

开发与打包
==========

* 代码风格基于 Cookiecutter Python Package 模板。
* 开发依赖可通过 ``pip install -r requirements_dev.txt`` 安装。
* 文档位于 ``docs/``，使用 Sphinx 构建：

  .. code-block:: console

     cd docs
     make html

许可证
======

本项目以 MIT 许可证发布，详情见 ``LICENSE``。

