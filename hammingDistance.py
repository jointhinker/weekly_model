def hammDis(x,y):
    if type(x) == int and type(y) == int:
        bx = bin(x).replace('0b', '')
        by = bin(y).replace('0b', '')
        #bxy = bin(x & y).replace('0b', '')
        
        l = len(by)
        if len(bx)>len(by):
            l = len(bx)
            add_zero = (l - len(by))*'0'
            by_total = add_zero + by
            bx_total = bx
        else:
            add_zero = (l - len(bx))*'0'
            bx_total = add_zero + bx
            by_total = by
        num = 0
        for i in range(l):
            if bx_total[i] != by_total[i]:
                num += 1
        return num
    else:
        return 'input type error'

x = input()
y = input()
print hammDis(x, y)
