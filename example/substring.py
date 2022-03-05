
ar = [
    "1234567890",
    "abcdefghijklmnop"
]



def main():
    s = "1234567890"
    s1 = s[0: 8]
    s2 = s[0: 22]
    s3 = ar[1]
    s3.capitalize()
    print("{} {}".format(s1, s2))

main()