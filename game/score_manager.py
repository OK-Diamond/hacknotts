import os

HIGH_SCORE_FILE = "highscore.txt"

def load_high_score():
    """Reads the high score from the text file"""
    if not os.path.exists(HIGH_SCORE_FILE):
        return 0
    
    with open(HIGH_SCORE_FILE, "r") as file:
        try:
            return int(file.read().strip())
        except ValueError:
            return 0  

def save_high_score(current_score):
    """Saves the score only if it beats the current record"""
    high_score = load_high_score()
    
    if current_score > high_score:
        with open(HIGH_SCORE_FILE, "w") as file:
            file.write(str(current_score))
        return True  
    return False
