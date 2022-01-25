f = 'hello \n hello again \n hello a \n'
g = f
f = f.replace('\n','')
print(f)
# g = g.split('\n')
h = ['1 ', ' 2', ' 3 ']


print([word.lstrip().rstrip() for word in g.split('\n')])

x = ' hello '
print('!' + x.rstrip().lstrip() + '!')
