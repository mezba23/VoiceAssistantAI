
s="six "
x={"one":1,"two":2,"three":3,"four":4,"five":5,"six":6,"seven":7,"eight":8,"nine":9,"zero":0}
lis=s.split(' ')

k=list(x.keys())
k.sort()
lis.sort()
print(k)
print(lis)
v=list(set(k).intersection(lis))
print (list(set(k).intersection(lis)))
print(v[0])
z=str(v[0])
print(x.get(z))
