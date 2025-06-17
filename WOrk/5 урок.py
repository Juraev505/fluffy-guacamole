numb = [i for i in range(101)]
print(numb)
number = [i for i in range(0,21,2)]
print(number)
names = ['Alex', 'Mike', 'Ivan', 'Eugene']
names2 = [h for h in names if "a" in h]
print(names2)
by = ['Pavel', 'Anton', 'Vasiliy']
my = [n[2] for n in by]
print(my)
bmu = [v for v in range(101)]
bma = [q+2 for q in bmu]
print(bma)
numbers = list(range(1, 11))
squares_of_evens = [x**2 for x in numbers if x % 2 == 0]
print(squares_of_evens)
vmb = [s for s in [input('введи имя: ')]]
print(vmb)