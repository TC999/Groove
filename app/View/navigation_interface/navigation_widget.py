# coding:utf-8
import os

from app.components.scroll_area import ScrollArea
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPainter, QPen
from PyQt5.QtWidgets import QWidget

from .navigation_widget_base import NavigationWidgetBase
from .navigation_button import CreatePlaylistButton, PushButton, ToolButton
from .search_line_edit import SearchLineEdit


class NavigationWidget(NavigationWidgetBase):
    """ 侧边导航窗口 """

    searchSig = pyqtSignal(str)
    switchToPlaylistInterfaceSig = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        # 创建滚动区域
        self.scrollArea = ScrollArea(self)
        self.scrollWidget = ScrollWidget(self)
        # 创建搜索框
        self.searchLineEdit = SearchLineEdit(self)
        # 创建按钮
        self.__createButtons()
        # 初始化界面
        self.__initWidget()

    def __createButtons(self):
        """实例化按钮 """
        self.showBarButton = ToolButton(
            "app/resource/images/navigation_interface/GlobalNavButton.png", parent=self)
        self.myMusicButton = PushButton(
            "app/resource/images/navigation_interface/MusicInCollection.png", "我的音乐", (400, 60), self.scrollWidget)
        self.historyButton = PushButton(
            "app/resource/images/navigation_interface/Recent.png", "最近播放的内容", (400, 62), self.scrollWidget)
        self.playingButton = PushButton(
            "app/resource/images/navigation_interface/黑色导航栏正在播放.png", "正在播放", (400, 62), self.scrollWidget)
        self.playlistButton = PushButton(
            "app/resource/images/navigation_interface/黑色播放列表.png", "播放列表", (340, 60), self.scrollWidget)
        self.createPlaylistButton = CreatePlaylistButton(self.scrollWidget)
        self.settingButton = PushButton(
            "app/resource/images/navigation_interface/Settings.png", "设置", (400, 62), self)
        # 创建播放列表名字按钮
        self.__createPlaylistNameButtons(self.getPlaylistNames())
        # 设置当前按钮
        self.currentButton = self.myMusicButton
        # todo:设置可选中的按钮列表
        self._selectableButtons = [
            self.myMusicButton,
            self.historyButton,
            self.playingButton,
            self.playlistButton,
            self.settingButton,
        ] + self.playlistNameButtons
        # todo:设置可选中的按钮名字列表
        self._selectableButtonNames = [
            "myMusicButton",
            "historyButton",
            "playingButton",
            "playlistButton",
            "settingButton",
        ] + self.playlistNames

    def __initWidget(self):
        """ 初始化小部件 """
        self.resize(400, 800)
        self.setAttribute(Qt.WA_StyledBackground)
        self.setSelectedButton(self.myMusicButton.property('name'))
        # 将按钮的点击信号连接到槽函数
        self._connectButtonClickedSigToSlot()
        self.__connectPlaylistNameClickedSigToSlot()
        self.searchLineEdit.searchButton.clicked.connect(
            self._onSearchButtonClicked)
        # 初始化布局
        self.__initLayout()

    def __initLayout(self):
        """ 初始化布局 """
        self.scrollArea.move(0, 162)
        self.scrollArea.setWidget(self.scrollWidget)
        # 将按钮添加到滚动区域
        self.historyButton.move(0, 62)
        self.showBarButton.move(0, 40)
        self.playingButton.move(0, 124)
        self.playlistButton.move(0, 186)
        self.searchLineEdit.move(15, 108)
        self.createPlaylistButton.move(340, 186)
        self.settingButton.move(0, self.height() - 187)
        self.__addPlaylistNameButtonsToScrollWidget()
        # 调整滚动区域的高度
        self.__adjustScrollWidgetHeight()

    def resizeEvent(self, e):
        """ 调整小部件尺寸 """
        self.scrollArea.resize(self.width(), self.height() - 347)
        self.scrollWidget.resize(self.width(), self.scrollWidget.height())
        self.settingButton.move(0, self.height() - 62 - 115 - 10)

    def paintEvent(self, e):
        """ 绘制分隔符 """
        painter = QPainter(self)
        painter.setPen(QColor(0, 0, 0, 30))
        painter.drawLine(15, self.settingButton.y()-1,
                         self.width()-15, self.settingButton.y()-1)

    @staticmethod
    def getPlaylistNames():
        """ 扫描播放列表名字 """
        os.makedirs('app/Playlists', exist_ok=True)
        playlists = [
            i[:-5] for i in os.listdir("app/Playlists") if i.endswith(".json")
        ]
        return playlists

    def __addPlaylistNameButtonsToScrollWidget(self):
        """ 将播放列表名字按钮添加到滚动部件上 """
        for index, button in enumerate(self.playlistNameButtons):
            button.move(0, 246 + index * 62)
            button.show()

    def __adjustScrollWidgetHeight(self):
        """ 调整滚动部件的高度 """
        buttonHeight = 246 + 62 * len(self.playlistNames)
        height = self.height()-346 if self.height()-346 > buttonHeight else buttonHeight
        self.scrollWidget.resize(400, height)

    def updateWindow(self):
        """ 更新界面 """
        # 扫描播放列表
        playlistNames = self.getPlaylistNames()
        if playlistNames == self.playlistNames:
            return

        # 删除旧播放列表名字按钮
        while self.playlistNameButtons:
            self._selectableButtons.pop()
            self._selectableButtonNames.pop()
            button = self.playlistNameButtons.pop()
            button.deleteLater()

        # 创建新按钮
        self.__createPlaylistNameButtons(playlistNames)
        self._selectableButtonNames += playlistNames
        self._selectableButtons += self.playlistNameButtons
        self._connectButtonClickedSigToSlot()
        self.__connectPlaylistNameClickedSigToSlot()

        # 移动按钮
        self.__addPlaylistNameButtonsToScrollWidget()
        self.__adjustScrollWidgetHeight()
        self.update()

    def __createPlaylistNameButtons(self, playlistNames: list):
        """ 创建播放列表名字按钮 """
        self.playlistNames = playlistNames
        self.playlistNameButtons = [
            PushButton("app/resource/images/navigation_interface/黑色我喜欢_60_62.png",
                       i, (400, 62), self.scrollWidget)
            for i in playlistNames
        ]

    def __connectPlaylistNameClickedSigToSlot(self):
        """ 将播放列表名字按钮点击信号连接到槽函数 """
        for button in self.playlistNameButtons:
            name = button.property('name')
            button.clicked.connect(
                lambda checked, name=name: self.switchToPlaylistInterfaceSig.emit(name))

    def _onSearchButtonClicked(self):
        """ 搜索按钮点击槽函数 """
        text = self.searchLineEdit.text()
        if text:
            self.currentButton.setSelected(False)
            self.searchSig.emit(text)


class ScrollWidget(QWidget):
    """ 滚动部件 """

    def paintEvent(self, e):
        """ 绘制分隔符 """
        painter = QPainter(self)
        pen = QPen(QColor(0, 0, 0, 30))
        painter.setPen(pen)
        # 前两个参数为第一个坐标，后两个为第二个坐标
        painter.drawLine(15, 185, self.width() - 15, 185)