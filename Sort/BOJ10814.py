import sys

n = int(sys.stdin.readline())

member = []
for _ in range(n):
    age, name = sys.stdin.readline().split()
    member.append((int(age), name))

member.sort(key=lambda x: x[0])

for m in member:
    print(m[0], m[1])