
alist = ['apple pie', 'banana cake', 'blueberry pie', 'vanilla cake']

alist.sort()

print(alist)

# lambda parameters: expression

add = lambda x, y: x + y

print(add(2,3))

#Using lambda functions as a sort key
blist = ['apple pie', 'banana cake', 'blueberry pie', 'vanilla cake']

#food = apple pie
#food.split() = ['apple', 'pie']
#food.split()[1] = 'pie'

blist.sort(key = lambda food: food.split()[1])

print(blist)