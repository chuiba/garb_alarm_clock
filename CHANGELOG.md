# Changelog

## 1.0.0 (2026-07-26)

全面现代化改造：

- 界面从 PyQt5 迁移到 PySide6（Qt 6），弃用 pyuic 生成代码，改为手写响应式布局
- 网络层从 requests 迁移到 httpx，请求全部在后台线程执行，界面不再因网络请求卡顿
- 实现「提醒编号」功能：粉丝编号达到目标值时蜂鸣并弹窗提醒
- 打包体系迁移到 `pyproject.toml`（PEP 621）+ src 布局 + hatchling，移除
  `setup.py`、`setup.cfg`、`tox.ini`、`.travis.yml`、`requirements*.txt` 等历史配置
- 用 ruff 替代 flake8，重写测试为可运行的 pytest 用例（`httpx.MockTransport` 模拟接口）
- CI 迁移到 uv，测试矩阵覆盖 Python 3.10–3.13

## 0.2.1 (2025-09-21)

- 兼容最新 B 站装扮接口，请求自动携带浏览器头信息
- 更新文档，补充运行指南和使用说明
- 修复发布流程，通过 trusted publisher 发布到 PyPI
  （0.2.0 仅为版本号变更，未实际发布）

## 0.1.0 (2021-04-17)

- 首次发布
