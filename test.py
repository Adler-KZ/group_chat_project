def print_map(n,m,bombT):
    for i in range(n):
        for j in range(m):
            print(bombT[i][j],end = ' ')
        print('')

n, m = map(int, input().split())
bombT = [[0]*m for i in range(n)]

for i in range(int(input())):
    bombY,bombX = map(int,input().split())
    bombT[bombY-1][bombX-1] = '*'
    for i in range(-1,2):
        for j in range (-1,2):
            x , y = bombX+i-1,bombY+j-1    
            if 0<=y<n and 0<=x<m and bombT[y][x] != '*':
                bombT[y][x]+=1

print_map(n,m,bombT)