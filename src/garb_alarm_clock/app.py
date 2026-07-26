"""PySide6 图形界面：定时刷新装扮信息，到达目标编号时提醒。"""

from __future__ import annotations

import sys
from datetime import datetime

from PySide6.QtCore import QObject, QRunnable, Qt, QThreadPool, QTimer, Signal, Slot
from PySide6.QtGui import QBrush, QFont, QPalette, QPixmap
from PySide6.QtWidgets import (
    QApplication,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

from .api import GarbClient, GarbInfo

MIN_INTERVAL = 60  # 秒，避免访问频率过高触发接口限流
MAX_INTERVAL = 86400
DEFAULT_ITEM_ID = "4389"


class _WorkerSignals(QObject):
    finished = Signal(object)  # (GarbInfo, avatar_bytes | None, background_bytes | None)
    failed = Signal(str)


class _FetchWorker(QRunnable):
    """在线程池中拉取装扮信息与图片，避免阻塞界面。"""

    def __init__(self, client: GarbClient, item_id: str, with_images: bool) -> None:
        super().__init__()
        self.signals = _WorkerSignals()
        self._client = client
        self._item_id = item_id
        self._with_images = with_images

    @Slot()
    def run(self) -> None:
        try:
            info = self._client.fetch_info(self._item_id)
            avatar = background = None
            if self._with_images:
                if info.avatar_url:
                    avatar = self._client.fetch_image(info.avatar_url)
                if info.image_url:
                    background = self._client.fetch_image(info.image_url)
        except Exception as exc:  # 后台线程中的任何异常都上报给界面
            self.signals.failed.emit(str(exc))
        else:
            self.signals.finished.emit((info, avatar, background))


class MainWindow(QMainWindow):
    """装扮编号小闹钟主窗口。"""

    def __init__(self, client: GarbClient | None = None) -> None:
        super().__init__()
        self._client = client or GarbClient()
        self._pool = QThreadPool(self)
        self._worker: _FetchWorker | None = None
        self._background_pixmap: QPixmap | None = None
        self._running = False
        self._countdown = 0
        self._alarm_fired = False

        self._timer = QTimer(self)
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self._on_tick)

        self._build_ui()

    # ------------------------------------------------------------------ UI

    def _build_ui(self) -> None:
        self.setWindowTitle("装扮编号小闹钟")
        self.setMinimumSize(660, 320)

        central = QWidget(self)
        root = QHBoxLayout(central)
        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(16)

        # 左侧信息卡片：半透明底色，保证叠加在装扮背景图上仍可读
        card = QFrame(central)
        card.setObjectName("infoCard")
        card.setStyleSheet(
            "#infoCard { background: rgba(255, 255, 255, 200); border-radius: 12px; }"
        )
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(16, 16, 16, 16)
        card_layout.setSpacing(8)

        header = QHBoxLayout()
        self.avatar_label = QLabel(card)
        self.avatar_label.setFixedSize(48, 48)
        self.avatar_label.setScaledContents(True)
        header.addWidget(self.avatar_label)

        self.name_label = QLabel("装扮名称", card)
        name_font = QFont()
        name_font.setPointSize(14)
        name_font.setBold(True)
        self.name_label.setFont(name_font)
        header.addWidget(self.name_label, 1)
        card_layout.addLayout(header)

        card_layout.addWidget(QLabel("FANS NO.", card))
        self.number_label = QLabel("——", card)
        number_font = QFont()
        number_font.setPointSize(28)
        number_font.setBold(True)
        self.number_label.setFont(number_font)
        card_layout.addWidget(self.number_label)

        detail = QGridLayout()
        detail.setHorizontalSpacing(12)
        detail.addWidget(QLabel("剩余库存", card), 0, 0)
        self.stock_label = QLabel("——", card)
        detail.addWidget(self.stock_label, 0, 1)
        detail.addWidget(QLabel("最后更新", card), 1, 0)
        self.updated_label = QLabel("——", card)
        detail.addWidget(self.updated_label, 1, 1)
        detail.addWidget(QLabel("下次刷新", card), 2, 0)
        self.countdown_label = QLabel("——", card)
        detail.addWidget(self.countdown_label, 2, 1)
        detail.setColumnStretch(1, 1)
        card_layout.addLayout(detail)
        card_layout.addStretch(1)

        root.addWidget(card, 1)

        # 右侧控制面板
        panel = QWidget(central)
        panel_layout = QVBoxLayout(panel)
        panel_layout.setContentsMargins(0, 0, 0, 0)

        form = QFormLayout()
        self.item_id_edit = QLineEdit(DEFAULT_ITEM_ID, panel)
        self.item_id_edit.setPlaceholderText("装扮的 item_id")
        form.addRow("装扮编号", self.item_id_edit)

        self.alarm_spin = QSpinBox(panel)
        self.alarm_spin.setRange(0, 99_999_999)
        self.alarm_spin.setSpecialValueText("关闭")
        self.alarm_spin.setToolTip("粉丝编号达到该值时弹窗提醒，0 表示关闭")
        self.alarm_spin.valueChanged.connect(self._on_alarm_target_changed)
        form.addRow("提醒编号", self.alarm_spin)

        self.interval_spin = QSpinBox(panel)
        self.interval_spin.setRange(MIN_INTERVAL, MAX_INTERVAL)
        self.interval_spin.setValue(MIN_INTERVAL)
        self.interval_spin.setSuffix(" 秒")
        self.interval_spin.setToolTip(f"刷新间隔，最低 {MIN_INTERVAL} 秒，防止被接口限流")
        form.addRow("刷新间隔", self.interval_spin)
        panel_layout.addLayout(form)

        self.start_button = QPushButton("开始", panel)
        self.start_button.clicked.connect(self._on_start_clicked)
        panel_layout.addWidget(self.start_button)
        panel_layout.addStretch(1)

        root.addWidget(panel)
        self.setCentralWidget(central)
        self.statusBar().showMessage("输入装扮编号后点击「开始」")

    # ------------------------------------------------------------- 启停控制

    @Slot()
    def _on_start_clicked(self) -> None:
        if self._running:
            self._stop_monitoring()
        else:
            self._start_monitoring()

    def _start_monitoring(self) -> None:
        item_id = self.item_id_edit.text().strip()
        if not item_id:
            self.statusBar().showMessage("请先填写装扮编号")
            return
        self._running = True
        self._alarm_fired = False
        self._countdown = self.interval_spin.value()
        self.start_button.setText("停止")
        self.item_id_edit.setEnabled(False)
        self._schedule_fetch(with_images=True)
        self._timer.start()

    def _stop_monitoring(self) -> None:
        self._running = False
        self._timer.stop()
        self.start_button.setText("开始")
        self.item_id_edit.setEnabled(True)
        self.countdown_label.setText("——")
        self.statusBar().showMessage("已停止")

    @Slot()
    def _on_tick(self) -> None:
        if not self._running:
            return
        self._countdown -= 1
        if self._countdown <= 0:
            self._countdown = self.interval_spin.value()
            self._schedule_fetch(with_images=False)
        self.countdown_label.setText(f"{self._countdown} 秒后")

    # ------------------------------------------------------------- 数据获取

    def _schedule_fetch(self, *, with_images: bool) -> None:
        if self._worker is not None:
            return  # 上一次请求还没结束，跳过本轮
        item_id = self.item_id_edit.text().strip()
        worker = _FetchWorker(self._client, item_id, with_images)
        worker.signals.finished.connect(self._on_fetch_finished)
        worker.signals.failed.connect(self._on_fetch_failed)
        self._worker = worker
        self.statusBar().showMessage("正在刷新…")
        self._pool.start(worker)

    @Slot(object)
    def _on_fetch_finished(self, result: object) -> None:
        self._worker = None
        info, avatar, background = result
        self._apply_info(info)
        self._apply_images(avatar, background)
        self.statusBar().showMessage("刷新成功")
        self._check_alarm(info.fan_number)

    @Slot(str)
    def _on_fetch_failed(self, message: str) -> None:
        self._worker = None
        self.statusBar().showMessage(f"刷新失败：{message}")

    def _apply_info(self, info: GarbInfo) -> None:
        if info.name:
            self.name_label.setText(info.name)
        self.number_label.setText(f"{info.fan_number:06d}")
        if info.sale_surplus is not None and info.sale_quantity is not None:
            self.stock_label.setText(f"{info.sale_surplus} / {info.sale_quantity}")
        else:
            self.stock_label.setText("——")
        self.updated_label.setText(datetime.now().strftime("%Y/%m/%d %H:%M:%S"))

    def _apply_images(self, avatar: bytes | None, background: bytes | None) -> None:
        if avatar:
            pixmap = QPixmap()
            if pixmap.loadFromData(avatar):
                self.avatar_label.setPixmap(pixmap)
        if background:
            pixmap = QPixmap()
            if pixmap.loadFromData(background):
                self._background_pixmap = pixmap
                self._apply_background()

    def _apply_background(self) -> None:
        if self._background_pixmap is None:
            return
        scaled = self._background_pixmap.scaled(
            self.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        palette = self.palette()
        palette.setBrush(QPalette.ColorRole.Window, QBrush(scaled))
        self.setPalette(palette)

    # ---------------------------------------------------------------- 提醒

    @Slot(int)
    def _on_alarm_target_changed(self, _value: int) -> None:
        self._alarm_fired = False

    def _check_alarm(self, number: int) -> None:
        target = self.alarm_spin.value()
        if target <= 0 or self._alarm_fired or number < target:
            return
        self._alarm_fired = True
        self._notify_alarm(number, target)

    def _notify_alarm(self, number: int, target: int) -> None:
        QApplication.beep()
        self.raise_()
        self.activateWindow()
        QMessageBox.information(
            self,
            "编号提醒",
            f"粉丝编号已达到 {number:06d}（提醒编号 {target:06d}）！",
        )

    # ---------------------------------------------------------------- 生命周期

    def resizeEvent(self, event) -> None:
        super().resizeEvent(event)
        self._apply_background()

    def closeEvent(self, event) -> None:
        self._timer.stop()
        self._pool.waitForDone(3000)
        self._client.close()
        super().closeEvent(event)


def main() -> int:
    """应用入口。"""
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
