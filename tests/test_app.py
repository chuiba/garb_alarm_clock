"""界面冒烟测试：在 offscreen 模式下验证窗口逻辑，不发真实请求。"""

import os

import pytest

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")

QtWidgets = pytest.importorskip("PySide6.QtWidgets", reason="PySide6 不可用", exc_type=ImportError)

from garb_alarm_clock.api import GarbInfo  # noqa: E402
from garb_alarm_clock.app import MainWindow, _FetchWorker  # noqa: E402


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


@pytest.fixture
def started_workers(window, monkeypatch):
    """拦截线程池，记录被调度的 worker 而不真正执行。"""
    workers = []
    monkeypatch.setattr(window._pool, "start", lambda w: workers.append(w))
    return workers


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


def deliver(window, info, *, with_images=False):
    """模拟一次当前代数的抓取成功回调。"""
    worker = _FetchWorker(window._client, "4389", with_images, window._generation)
    window._on_fetch_finished(worker, (info, None, None))


def test_window_initial_state(window):
    assert window.windowTitle() == "装扮编号小闹钟"
    assert window.start_button.text() == "开始"
    assert window.item_id_edit.text() == "4389"
    assert window.interval_spin.value() == 60
    assert window.alarm_spin.value() == 0


def test_fetch_result_updates_labels(window):
    deliver(window, sample_info())

    assert window.name_label.text() == "测试装扮"
    assert window.number_label.text() == "000600"
    assert window.stock_label.text() == "400 / 1000"
    assert window.updated_label.text() != "——"


def test_fetch_failure_shows_status(window):
    worker = _FetchWorker(window._client, "4389", False, window._generation)
    window._on_fetch_failed(worker, "网络错误")
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
    deliver(window, sample_info(fan_number=499))
    assert calls == []

    deliver(window, sample_info(fan_number=600))
    assert calls == [600]

    # 同一目标不重复提醒
    deliver(window, sample_info(fan_number=700))
    assert calls == [600]

    # 修改目标后重新武装
    window.alarm_spin.setValue(650)
    deliver(window, sample_info(fan_number=700))
    assert calls == [600, 700]


def test_stop_resets_button(window, started_workers):
    window._start_monitoring()
    assert window._running
    assert window.start_button.text() == "停止"

    window._on_start_clicked()
    assert not window._running
    assert window.start_button.text() == "开始"


def test_stale_result_discarded_after_stop(window, started_workers, monkeypatch):
    calls = []
    monkeypatch.setattr(window, "_notify_alarm", lambda number, target: calls.append(number))
    window.alarm_spin.setValue(500)

    window._start_monitoring()
    stale = started_workers[-1]
    window._stop_monitoring()

    # 停止后才返回的在途结果：不更新界面、不触发提醒
    window._on_fetch_finished(stale, (sample_info(fan_number=600), None, None))
    assert window.number_label.text() == "——"
    assert calls == []
    assert "已停止" in window.statusBar().currentMessage()

    window._on_fetch_failed(stale, "旧请求失败")
    assert "旧请求失败" not in window.statusBar().currentMessage()


def test_restart_does_not_drop_initial_fetch(window, started_workers):
    window._start_monitoring()
    assert len(started_workers) == 1

    # 旧请求仍在途时停止并换一个装扮重新开始
    window._on_start_clicked()
    window.item_id_edit.setText("9999")
    window._on_start_clicked()

    assert len(started_workers) == 2
    assert started_workers[-1].item_id == "9999"
    assert started_workers[-1].with_images


def test_images_retried_until_first_success(window, started_workers):
    window._start_monitoring()
    first = started_workers[-1]
    assert first.with_images

    # 首次含图请求失败：下一轮继续带图重试
    window._on_fetch_failed(first, "412")
    window._countdown = 1
    window._on_tick()
    retry = started_workers[-1]
    assert retry.with_images

    # 含图请求成功一次后，后续轮询不再重复拉图
    window._on_fetch_finished(retry, (sample_info(), None, None))
    window._countdown = 1
    window._on_tick()
    assert not started_workers[-1].with_images
