=====
使用
=====

快速启动
--------

.. code-block:: console

   python -m garb_alarm_clock

界面说明
--------

* 装扮编号：输入装扮 ``item_id``，点击 ``开启`` 按钮后立即刷新。
* 提醒编号：可记录粉丝编号或个人提醒信息，当前逻辑不会自动使用。
* 刷新间隔：倒计时结束时会重新访问接口，最小值限制为 60 秒。
* 主界面背景、头像和粉丝编号会同步更新；窗口右下角显示最后刷新时间。

二次开发
--------

如需在代码中复用装扮查询能力，可直接调用 ``garb_alarm_clock.garb`` 模块：

.. code-block:: python

   from garb_alarm_clock import garb

   name, image_url, avatar_url, surplus, quantity, number = garb.get_garb_info(4389)

接口调用会自动附带浏览器请求头并处理库存缺失的情况。
