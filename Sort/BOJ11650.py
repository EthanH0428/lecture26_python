import sys

n = int(sys.stdin.readline())

points = []
for _ in range(n):
    x, y = map(int, sys.stdin.readline().split())
    points.append((x, y))

points.sort()

for pt in points:
    print(pt[0], pt[1])