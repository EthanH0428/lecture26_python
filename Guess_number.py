import random

num_limit = 50
try_limit = int(input('몇 번 안에 맞출까? :'))
rand_num = random.randint(1, num_limit)
shot_num = _
attempt = 1

while True :
    if attempt > try_limit :
        print('Limit Over! The number was', rand_num)
        break
    shot_num = int(input('give a shot! : '))

    if (shot_num < rand_num) :
        print('up')
    elif (shot_num > rand_num) :
        print('down')
    else :
        print(f'U Win! (in {attempt} turn, the Answer was {rand_num})')
        break
        
    attempt += 1