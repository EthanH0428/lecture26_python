# 1. 자료구조
# 화면에 보여줄 보드
board_screen = ' 0 | 1 | 2 \n 3 | 4 | 5 \n 6 | 7 | 8\n '
# 게임의 진행 상태
board = [""] * 9
win_status = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
human = 'O'
computer = 'X'
# 2. 필요한 함수 정의
def showBoard():
    print(board_screen)

def updateGame(who, number):
    global board, board_screen
    board[number] = who
    board_screen = board_screen .replace(str(number), who)
    

def getComputerNumber():
    for i in range(len(board)):
        if board[i] == " ":
            return i
    return -1

def isWin(turn):
    for status in win_status:
        if board[status[0]] == board[status[1]] == board[status[2]] == turn:
            return True
    return False

# 3. 메인 로직
# 3-1. 필요한 자료구조 초기화
print('==============Tic-Tac-Toe==============')
showBoard()
while True:
    # 3-2. 보드를 보여줌
    # 3-3. human 차례
    human_input = int(input('숫자를 입력하세요'))
    updateGame(human, human_input)
    showBoard()

    if isWin(human):
        print('You Win~~!!')
        # break
    # 3-4. 컴퓨터 차례
    computer_input = getComputerNumber()
    if computer_input == -1:
        print('The game ended in a tie~~!!')
        break
    updateGame(computer, computer_input)
    showBoard()
    if isWin(computer):
        print('You loose~~~') 
        break