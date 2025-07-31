# スコアの初期化
_current_score = 0

def reset_score():
    global _current_score
    _current_score = 0

def add_score(points: int):
    global _current_score
    _current_score += points

def get_score() -> int:
    return _current_score
