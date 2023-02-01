!usr/bin/python env

steps = ((0,1), (1,1), (1,0), (1,-1), (0,-1),(-1,-1),(-1,0),(-1,1))


def bfs(x,y,W,H):

	que.append((x,y))

	x,y = que.pop()
	visited[x][y] = 1

	for i,j in steps:
		x1 = x + i
		y1 = y + j

		if x1<0 or x1>=W or y1<0 or y1>=H:
			continue

		if visited[x1][y1] == 1:
			continue

		visited[x1][y1] =1
		
		


	

	