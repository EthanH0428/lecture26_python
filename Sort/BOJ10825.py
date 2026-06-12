import sys

n = int(sys.stdin.readline())

students = []
for _ in range(n):
    name, kor, eng, math = sys.stdin.readline().split()
    students.append((name, int(kor), int(eng), int(math)))

students.sort(key=lambda x: (-x[1], x[2], -x[3], x[0]))

for student in students:
    print(student[0])