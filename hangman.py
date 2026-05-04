import random

word_list = ["MAN", "GANG", "HANG", "APPLE", "BANANA", "DOG", "CAT", "BIRD", "BOOK", "DESK", "PARK", "SUN", "MOON"]

rand_index = random.randint(0, len(word_list) - 1)
word = word_list[rand_index]

ans = ["_"] * len(word)


def test(word):
    print(word)


def start_hangman(word):
    print("===========HANG-MAN===========")

    test(word)

    print(" ".join(ans), "(" + str(len(word)) + "글자)")

    for i in range(1,len(word) + 5):
        user_input = input("알파벳 입력: ").upper()

        if user_input in word:
            for j in range(len(word)):
                if word[j] == user_input:
                    ans[j] = user_input

            print("맞음"+str(len(word) + 9 - i)+"번 남았습니다")
        else:
            print("틀림"+str(len(word) + 9 - i)+"번 남았습니다")

        print(" ".join(ans))

        if "_" not in ans:
            print("이겼습니다")
            break
        if i==len(word) + 9:
            print("해결하지 못했습니다")


start_hangman(word)