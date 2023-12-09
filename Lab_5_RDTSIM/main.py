
print('Implementing a Reliable Transport Protocol')
try:
    num = int(input('Select 1(Alternating-Bit-Protocol) or 2 (Go-Back-N): '))

    if num == 1:
        print('\n\nAlternating-Bit-Protocol Version \n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        exec(open('Lab_5_RDTSIM/rdtsim_alternating_bit.py').read())
    elif num == 2:
        print('\n\nGo-Back-N Version \n>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>\n')
        exec(open('Lab_5_RDTSIM/rdtsim_go_back_n.py').read())
    else:
        print('Error. You must select 1 or 2')
except Exception as e:
    print('invalid')
    print(e)
