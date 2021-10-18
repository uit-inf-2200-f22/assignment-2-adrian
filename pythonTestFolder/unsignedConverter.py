# Courtesy https://stackoverflow.com/questions/38935169/convert-elements-of-a-list-into-binary
def main():
    num = -100
    print(num)
    word = list(bin(num)[2:])
    word[0] = '0'

    num2 = 0
    i = 0
    print(int(word[1]))
    for b in word:
        num2 = num2 + int(word[0])*((len(word)-i)**2)
        i += 1

    num = ''.join(map(str,word))
    
    print(num2)
    print(num)



    # i = 0
    # for j in word:
    #     num = 2*num+j

    # print(i)

if __name__ == "__main__":
    main()