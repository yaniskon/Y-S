while True:
    try:
        print("You can enter 1,2,3,4")
        x= int(input('enter a menu number: '))
        if x == 4:
            print("Quit program")
            break
        elif x == 1:
            print('1 Selected')
        elif x == 2 :
            print('2 selected')
        elif x ==3:
            print('3 selected')
        else:
            print('option not valid')
    except ValueError:
        print('Error')