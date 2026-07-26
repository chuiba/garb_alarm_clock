"""界面冒烟测试：在 offscreen 模式下验证窗口逻辑，不发真实请求。"""

import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

QtWidgets = pytest.importorskip("PySide6.QtWidgets", reason="PySide6 不可用", exc_type=ImportError)

from garb_alarm_clock.api import GarbInfo  # noqa: E402
from garb_alarm_clock.app import MainWindow  # noqa: E402


@pytest.fixture(scope="session")
def qapp():
    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    yield app


@pytest.fixture
def window(qapp):
    win = MainWindow()
    yield win
    win._client.close()
    win.deleteLater()


def sample_info(**overrides):
    values = {
        "name": "测试装扮",
        "image_url": "",
        "avatar_url": "",
        "sale_surplus": 400,
        "sale_quantity": 1000,
        "fan_number": 600,
    }
    values.update(overrides)
    return GarbInfo(**values)


def test_window_initial_state(window):
    assert window.windowTitle() == "装扮编号小闹钟"
    assert window.start_button.text() == "开始"
    assert window.item_id_edit.text() == "4389"
    assert window.interval_spin.value() == 60
    assert window.alarm_spin.value() == 0


def test_fetch_result_updates_labels(window):
    window._on_fetch_finished((sample_info(), None, None))

    assert window.name_label.text() == "测试装扮"
    assert window.number_label.text() == "000600"
    assert window.stock_label.text() == "400 / 1000"
    assert window.updated_label.text() != "——"


def test_fetch_failure_shows_status(window):
    window._on_fetch_failed("网络错误")
    assert "网络错误" in window.statusBar().currentMessage()


def test_empty_item_id_blocks_start(window):
    window.item_id_edit.setText("  ")
    window._on_start_clicked()
    assert not window._running
    assert window.start_button.text() == "开始"


def test_alarm_fires_once_when_target_reached(window, monkeypatch):
    calls = []
    monkeypatch.setattr(window, "_notify_alarm", lambda number, target: calls.append(number))

    window.alarm_spin.setValue(500)
    window._on_fetch_finished((sample_info(fan_number=499), None, None))
    assert calls == []

    window._on_fetch_finished((sample_info(fan_number=600), None, None))
    assert calls == [600]

    # 同一目标不重复提醒
    window._on_fetch_finished((sample_info(fan_number=700), None, None))
    assert calls == [600]

    # 修改目标后重新武装
    window.alarm_spin.setValue(650)
    window._on_fetch_finished((sample_info(fan_number=700), None, None))
    assert calls == [600, 700]


def test_stop_resets_button(window, monkeypatch):
    monkeypatch.setattr(window, "_schedule_fetch", lambda **kwargs: None)
    window._start_monitoring()
    assert window._running
    assert window.start_button.text() == "停止"

    window._on_start_clicked()
    assert not window._running
    assert window.start_button.text() == "开始"
