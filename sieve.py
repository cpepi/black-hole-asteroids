num = int(input("number 2+ please "))

li = list(range(2,num + 1))

while(li):
    val = li.pop(0)
    print (val)
    rem = []
    for i in range(len(li) - 1, 0, -1):
        if li[i] % val == 0:
            rem.append(li.pop(i))
    if rem:
        print("non primes removed: {0}".format(rem[::-1]))
