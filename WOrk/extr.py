unit = input('Выберите единицу измерения(метры,футы): ')
if unit == 'метры':
   lenght = float(input('Введите длину: '))
   width = float(input('Введите ширину: '))
   print("площадь комнаты =", lenght * width,'метров^2')
elif unit == 'футы':
    lenght = float(input('Введите длину: '))
    width = float(input('Введите ширину: '))
    print("площадь комнаты =", lenght*width, 'футов^2' )
else:
    print("недоступная информация")



