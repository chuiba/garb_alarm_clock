.. highlight:: shell

============
安装指南
============

本节介绍如何在本地环境中运行 B 站装扮小闹钟。

准备工作
--------

* Python 3.9 及以上版本
* Git（用于克隆仓库，可选）
* 能访问 ``https://api.bilibili.com`` 的网络环境

获取代码
--------

.. code-block:: console

   git clone https://github.com/chuiba/garb_alarm_clock.git
   cd garb_alarm_clock

依赖安装
--------

推荐使用虚拟环境隔离依赖：

.. code-block:: console

   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # macOS / Linux
   pip install PyQt5 requests

如需进行开发或运行测试，可额外安装 ``requirements_dev.txt`` 中的依赖：

.. code-block:: console

   pip install -r requirements_dev.txt

启动应用
--------

.. code-block:: console

   python -m garb_alarm_clock

运行后会弹出 PyQt5 界面；如果通过远程/无桌面环境运行，请确保启用了合适的显示服务。

升级与维护
----------

* 若 B 站接口再次调整，可在 ``garb_alarm_clock/garb.py`` 中更新请求头。
* 依赖更新后，如遇到安装问题，可重新创建虚拟环境并安装最新依赖。
