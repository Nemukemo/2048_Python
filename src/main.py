#!/usr/bin/env python3
"""
2048ゲーム メインエントリーポイント
GUIで2048ゲームを起動
"""

import sys
import os
import importlib.util

# 現在のディレクトリをパスに追加
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """GUIで2048ゲームを起動"""
    try:
        # wxPythonの可用性をチェック
        import wx
        
        # 数字で始まるモジュール名のため、動的インポートを使用
        gui_path = os.path.join(os.path.dirname(__file__), "game_ui", "2048_board.py")
        
        if not os.path.exists(gui_path):
            print(f"エラー: GUIファイルが見つかりません: {gui_path}")
            input("Enterキーを押して終了...")
            return
        
        spec = importlib.util.spec_from_file_location("board_2048", gui_path)
        board_2048 = importlib.util.module_from_spec(spec)
        
        # モジュールを実行
        spec.loader.exec_module(board_2048)
        
        # wxAppを作成してGUIを起動
        app = wx.App(False)
        frame = board_2048.GameBoard(None, title="2048 Game")
        app.MainLoop()
        
    except ImportError as e:
        print("エラー: wxPythonがインストールされていません")
        print("以下のコマンドでインストールしてください:")
        print("conda activate py39")
        print("conda install wxpython")
        print("または")
        print("pip install wxpython")
        print(f"\n詳細: {e}")
        input("Enterキーを押して終了...")
    except Exception as e:
        print(f"エラー: ゲーム実行中に問題が発生しました: {e}")
        import traceback
        traceback.print_exc()
        input("Enterキーを押して終了...")

if __name__ == "__main__":
    main()
