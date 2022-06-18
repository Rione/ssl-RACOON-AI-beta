#!/usr/bin/env python3.10

"""animated_toggle.py

   This module contains:
       - AnimatedToggle
"""

from typing import Optional

from PyQt6.QtCore import pyqtProperty  # type: ignore # pylint: disable=E0611
from PyQt6.QtCore import (  # pylint: disable=E0611
    QByteArray,
    QEasingCurve,
    QPoint,
    QPointF,
    QPropertyAnimation,
    QRectF,
    QSequentialAnimationGroup,
    QSize,
    Qt,
    pyqtSlot,
)
from PyQt6.QtGui import QBrush, QColor, QPainter, QPaintEvent, QPen  # pylint: disable=E0611
from PyQt6.QtWidgets import QCheckBox, QWidget  # pylint: disable=E0611


class AnimatedToggle(QCheckBox):
    """AnimatedToggle

    Args:
        parent (Optional[QWidget]): The parent widget of the AnimatedToggle.
        bar_color (str, optional): The color of the bar. Defaults to "#808080".
        checked_color (str, optional): The color of the bar when checked. Defaults to "#00B0FF".
        handle_color (str, optional): The color of the handle. Defaults to "#FFFFFF".
        pulse_unchecked_color (str, optional): The color of the pulse when unchecked. Defaults to "#44999999".
        pulse_checked_color (str, optional): The color of the pulse when checked. Defaults to "#4400B0EE".
    """

    _transparent_pen = QPen(Qt.GlobalColor.transparent)
    _light_grey_pen = QPen(Qt.GlobalColor.lightGray)

    def __init__(
        self,
        parent: Optional[QWidget],
        bar_color: str = "#808080",
        checked_color: str = "#00B0FF",
        handle_color: str = "#FFFFFF",
        pulse_unchecked_color: str = "#44999999",
        pulse_checked_color: str = "#4400B0EE",
    ) -> None:
        super().__init__(parent)

        # Save our properties on the object via self, so we can access them later
        # in the paintEvent.
        self._bar_brush: QBrush = QBrush(QColor(bar_color))
        self._bar_checked_brush: QBrush = QBrush(QColor(checked_color).lighter())

        self._handle_brush: QBrush = QBrush(QColor(handle_color))
        self._handle_checked_brush: QBrush = QBrush(QColor(checked_color))

        self._pulse_unchecked_animation: QBrush = QBrush(QColor(pulse_unchecked_color))
        self._pulse_checked_animation: QBrush = QBrush(QColor(pulse_checked_color))

        # Setup the rest of the widget.
        self.setContentsMargins(8, 0, 8, 0)
        self.__handle_position: float = float(0)

        self.__pulse_radius: float = float(0)

        self.animation: QPropertyAnimation = QPropertyAnimation(
            self,
            QByteArray(b"handle_position"),  # type: ignore
            self,
        )
        self.animation.setEasingCurve(QEasingCurve.Type.InOutCubic)
        self.animation.setDuration(200)  # time in ms

        self.pulse_anim: QPropertyAnimation = QPropertyAnimation(
            self,
            QByteArray(b"pulse_radius"),  # type: ignore
            self,
        )
        self.pulse_anim.setDuration(350)  # time in ms
        self.pulse_anim.setStartValue(10)
        self.pulse_anim.setEndValue(20)

        self.animations_group = QSequentialAnimationGroup()
        self.animations_group.addAnimation(self.animation)
        self.animations_group.addAnimation(self.pulse_anim)

        self.stateChanged.connect(self.setup_animation)  # type: ignore

    def sizeHint(self) -> QSize:  # pylint: disable=C0103,R0201
        """sizeHint"""
        return QSize(58, 45)

    def hitButton(self, pos: QPoint) -> bool:  # pylint: disable=C0103
        """hitButton"""
        return self.contentsRect().contains(pos)

    @pyqtSlot(int)  # type: ignore
    def setup_animation(self, value: Optional[int]) -> None:
        """setup_animation"""
        self.animations_group.stop()
        if value:
            self.animation.setEndValue(1)
        else:
            self.animation.setEndValue(0)
        self.animations_group.start()

    def paintEvent(self, _: QPaintEvent) -> None:  # pylint: disable=C0103
        """paintEvent"""
        # pylint: disable=C0103
        contRect = self.contentsRect()
        handleRadius = round(0.24 * contRect.height())

        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        p.setPen(self._transparent_pen)
        barRect = QRectF(0, 0, contRect.width() - handleRadius, 0.40 * contRect.height())
        temp = QPointF(float(contRect.center().x()), float(contRect.center().y()))
        barRect.moveCenter(temp)
        rounding = barRect.height() / 2

        # the handle will move along this line
        trailLength = contRect.width() - 2 * handleRadius

        xPos = contRect.x() + handleRadius + trailLength * self.__handle_position

        if self.pulse_anim.state() == QPropertyAnimation.State.Running:
            p.setBrush(self._pulse_checked_animation if self.isChecked() else self._pulse_unchecked_animation)
            p.drawEllipse(QPointF(xPos, barRect.center().y()), self.__pulse_radius, self.__pulse_radius)

        if self.isChecked():
            p.setBrush(self._bar_checked_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setBrush(self._handle_checked_brush)

        else:
            p.setBrush(self._bar_brush)
            p.drawRoundedRect(barRect, rounding, rounding)
            p.setPen(self._light_grey_pen)
            p.setBrush(self._handle_brush)

        p.drawEllipse(QPointF(xPos, barRect.center().y()), handleRadius, handleRadius)

        p.end()

    @pyqtProperty(float)
    def handle_position(self) -> float:
        """handle_position"""
        return self.__handle_position

    @handle_position.setter
    def handle_position(self, pos: float) -> None:
        """change the property
        we need to trigger QWidget.update() method, either by:
            1- calling it here [ what we doing ].
            2- connecting the QPropertyAnimation.valueChanged() signal to it.
        """
        self.__handle_position = float(pos)
        self.update()

    @pyqtProperty(float)
    def pulse_radius(self) -> float:
        """pulse_radius"""
        return self.__pulse_radius

    @pulse_radius.setter
    def pulse_radius(self, pos: float) -> None:
        """pulse_radius"""
        self.__pulse_radius = float(pos)
        self.update()
