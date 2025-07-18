import wx

class MyFrame(wx.Frame):
    def __init__(self, *args, **kw):
        super(MyFrame, self).__init__(*args, **kw)

        self.panel = wx.Panel(self)

        # メイン縦方向のsizer（sizer2相当）
        main_sizer = wx.BoxSizer(wx.VERTICAL)

        # ==== スコア部分 ====
        self.score_text = wx.StaticText(self.panel, label="Score: 0")
        font = self.score_text.GetFont()
        font.PointSize += 8
        font = font.Bold()
        self.score_text.SetFont(font)

        # スコア部分を中央に固定し、最小高さ確保
        main_sizer.Add(self.score_text, proportion=0, flag=wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, border=10)

        # ==== グリッド部分 ====
        grid_sizer = wx.GridSizer(4, 4, 5, 5)

        # 16マス作成（ただのプレースホルダー）
        for i in range(16):
            tile = wx.Panel(self.panel, size=(60, 60))
            tile.SetBackgroundColour(wx.Colour(220, 220, 220))  # 薄いグレー
            grid_sizer.Add(tile, 1, flag=wx.EXPAND)

        # グリッド部分をexpandさせる
        main_sizer.Add(grid_sizer, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        self.panel.SetSizer(main_sizer)
        self.Centre()
        self.SetSize((400, 500))
        self.Show()

if __name__ == '__main__':
    app = wx.App(False)
    frame = MyFrame(None, title="2048 Game")
    app.MainLoop()
