"""
n, k, a, b, d.
"""
"""
n, k, a, b, d = map(int,input().split())

graph = [ [] for _ in range(n) ]

for _ in range(k):
	x,y = map(int,input().split())
	graph[x-1].append(y-1)
"""
count = 0

degs = []

#print(graph)

def dfs(graph,a,b,d,path):
	global count, deg
	print(a)
	path.append(a)	
	if d==0:
		count += 1
		vals = []
		for day in path:
			for el in graph[day]:
				if el in path:
					continue
				if el in vals:
					continue
				vals.append(el) 
		degs.append(vals)
		return
	
	
	print("path:",path)
	print(a,graph)	
	for next in graph[a]:
		if next in path:
			continue
		dfs(graph,next,b,d-1,path)

#dfs(graph,a-1,b-1,2,[])
#print(count, degs)


degrees = []



def dfs2(W,H, x0,y0,d,path=[]):

	global degrees
	steps = ((0,1), (1,1), (1,0), (1,-1), (0,-1),(-1,-1),(-1,0),(-1,1))
	
	print("xy",x0,y0)
	v = W*y0 + x0
	path.append(v) 
	if len(path)==d: 
		print("path f:",path)
		vals = []
		for cell in path:
			for nb in steps:
				x1 = cell % W + nb[0] 
				y1 = cell // W + nb[1]
				
				if x1<0 or x1>=W or y1<0 or y1>=H:
					continue
				val = W * y1 + x1
				if val in path:
					continue
				if val in vals:
					continue
				vals.append(val)
		degrees.append(len(vals))
		print("v:",vals)
		return
	print("s=",x0,y0,v, path)
	for nb in steps:
		x1 = x0 + nb[0]
		y1 = y0 + nb[1]
		if x1<0 or x1>=W or y1<0 or y1>=H:
			continue
		v1 = W*y1 + x1
		print("v1",v1)
		if v1 in path:
			continue
		dfs2(W,H,x1,y1,d,path)
		path.pop(-1)
				  		

dfs2(6,3,0,0,2,[])
print(degrees)