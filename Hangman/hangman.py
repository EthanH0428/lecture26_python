import random
class Hangman:
    MAX_TRY = 7
    MASK_CHAR = '_'
    RIGHT = 1
    WRONG = 0
    ERROR = -1
    WIN = 1
    LOOSE = 0
    CONTINUE = -1
    
    def __init__(self, word_list):
        self.word = random.choice(word_list).upper()
        self.display_word = Hangman.MASK_CHAR * len(self.word)
        self.num_try = 0
        self.input_letters = []
        self.error_status = ''

    def check_letter(self, letter):
        if not letter.isalpha():
            self.error_status = '알파벳을 입력하시오'
            return Hangman.ERROR

        letter = letter.upper()
        # 이미 입력했던 문자인지 확인
        if letter in self.input_letters:
            self.error_status = f'이미 입력한 알파벳입니다 {self.input_letters}'
            return Hangman.ERROR  
        self.input_letters.append(letter)    

        if self.word.count(letter) > 0: 
            # 있는 문자이면 display_word에서 위치를 찾아 수정
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.display_word = self.display_word[:i] + letter + self.display_word[i+1:]
            return Hangman.RIGHT
        else:
            self.num_try += 1
            return Hangman.WRONG
    
    def is_win(self):
        # 이겼을 때
        if self.display_word.count(Hangman.MASK_CHAR) == 0:
            return Hangman.WIN
        # 졌을 때
        elif self.num_try >= Hangman.MAX_TRY:
            return Hangman.LOOSE

        return Hangman.CONTINUE