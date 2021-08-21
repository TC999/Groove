# coding:utf-8

from app.components.selection_mode_bar_base import (BasicButton,
                                                    SelectionModeBarBase,
                                                    CheckAllButton)


class SelectionModeBar(SelectionModeBarBase):
    """ 选择状态工具栏 """

    def __init__(self, parent=None):
        super().__init__(parent)
        # 创建按钮
        self.__createButtons()
        # 初始化界面
        self.__initWidget()

    def __createButtons(self):
        """ 创建按钮 """
        self.cancelButton = BasicButton(
            r"app\resource\images\selection_mode_bar\Cancel.png", "取消", self
        )
        self.playButton = BasicButton(
            r"app\resource\images\selection_mode_bar\Play.png", "播放", self
        )
        self.nextToPlayButton = BasicButton(
            r"app\resource\images\selection_mode_bar\下一首播放_20_20.png", "下一首播放", self
        )
        self.addToButton = BasicButton(
            r"app\resource\images\selection_mode_bar\Add.png", "添加到", self
        )
        self.renameButton = BasicButton(
            r"app\resource\images\selection_mode_bar\Edit.png", "重命名", self
        )
        self.pinToStartMenuButton = BasicButton(
            r"app\resource\images\selection_mode_bar\Pin.png",
            '固定到"开始"菜单',
            self,
        )
        self.deleteButton = BasicButton(
            r"app\resource\images\selection_mode_bar\Delete.png", "删除", self
        )
        self.checkAllButton = CheckAllButton(
            [
                r"app\resource\images\selection_mode_bar\SelectAll.png",
                r"app\resource\images\selection_mode_bar\取消全选_20_20.png",
            ],
            ["全选", "取消全选"],
            self,
        )

    def __initWidget(self):
        """ 初始化界面 """
        self.addButtons(
            [
                self.cancelButton,
                self.playButton,
                self.nextToPlayButton,
                self.addToButton,
                self.renameButton,
                self.pinToStartMenuButton,
                self.deleteButton,
                self.checkAllButton,
            ]
        )
        self.setToHideButtons(self.button_list[4:6])
        self.insertSeparator(1)