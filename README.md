# garb-alarm-clock

B 站装扮编号小闹钟：定时刷新并展示指定装扮的信息（名称、粉丝编号、头像、剩余库存），并在粉丝编号到达目标值时弹窗提醒。

项目最初开发于 2021 年，1.0 版本完成了全面现代化改造：

- **界面**：PyQt5 → PySide6（Qt 6 官方绑定，LGPL 许可，与本项目 MIT 许可兼容），手写响应式布局
- **网络**：requests → httpx，所有请求在后台线程执行，界面不再卡顿
- **提醒**：真正实现了「提醒编号」功能——粉丝编号达到目标值时蜂鸣并弹窗
- **工程**：`pyproject.toml` + src 布局 + uv + ruff + pytest，CI 覆盖 Python 3.10–3.13

## 安装

```console
pip install garb-alarm-clock
```

或从源码运行（推荐使用 [uv](https://docs.astral.sh/uv/)）：

```console
git clone https://github.com/chuiba/garb_alarm_clock.git
cd garb_alarm_clock
uv run garb-alarm-clock
```

Windows 用户也可以直接从 [Releases](https://github.com/chuiba/garb_alarm_clock/releases) 下载免安装的 `garb_alarm_clock.exe`。

## 使用说明

启动后在右侧面板填写：

- **装扮编号**：装扮的 `item_id`，可以从装扮页面 URL 中找到
- **提醒编号**：粉丝编号达到该值时弹窗提醒，`0` 表示关闭提醒
- **刷新间隔**：单位为秒，最低 60 秒，防止请求过于频繁被接口限流

点击「开始」后会立刻加载装扮名称、头像、背景图和当前粉丝编号，之后按设定间隔自动刷新编号。点击「停止」结束监控。

## 接口兼容性

B 站在 2023 年之后对装扮接口增加了浏览器校验。本项目在 `api.py` 中携带了浏览器标识头，二次开发请保留 `User-Agent`、`Origin`、`Referer` 这些请求头。若出现 412 错误，可尝试：

- 确认本地网络未拦截 `https://api.bilibili.com`
- 调大刷新间隔，避免短时间内请求过多
- 把 `User-Agent` 换成当前常用浏览器的值

## 开发

```console
uv sync              # 安装依赖（含开发依赖）
uv run pytest        # 运行测试（无显示环境时加 QT_QPA_PLATFORM=offscreen）
uvx ruff check .     # 代码检查
uvx ruff format .    # 代码格式化
uv build             # 构建 sdist 和 wheel
```

打包 Windows 可执行文件：

```console
uv run --with pyinstaller pyinstaller garb_alarm_clock.spec --clean
```

## 许可证

本项目以 [MIT 许可证](LICENSE)发布。
