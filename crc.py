import sys
def xor(a, b):
    result = ""
    for i in range(1, len(b)):
        if a[i] == b[i]:
            result += "0"
        else:
            result += "1"
    return result

def mod2div(dividend, divisor):
    pick = len(divisor)
    temp = dividend[0:pick]

    while pick < len(dividend):
        if temp[0] == '1':
            temp = xor(divisor, temp) + dividend[pick]
        else:
            temp = xor('0' * len(divisor), temp) + dividend[pick]
        pick += 1

    if temp[0] == '1':
        temp = xor(divisor, temp)
    else:
        temp = xor('0' * len(divisor), temp)

    return temp

def encode_crc(data, generator):
    appended_data = data + '0' * (len(generator) - 1)
    remainder = mod2div(appended_data, generator)
    codeword = data + remainder
    return remainder, codeword

def decode_crc(codeword, generator):
    remainder = mod2div(codeword, generator)
    if '1' in remainder:
        return False
    return True

print("----- CRC CHECKSUM PROGRAM -----")

data = input("Enter data bits: ")
generator = input("Enter generator bits: ")

remainder, codeword = encode_crc(data, generator)

print("\nSender Side")
print("CRC Remainder :", remainder)
print("Codeword      :", codeword)

print("\nReceiver Side")
if decode_crc(codeword, generator):
    print("No Error Detected")
else:
    print("Error Detected")

corrupted = codeword[:-1] + ('1' if codeword[-1] == '0' else '0')

print("\nCorrupted Codeword :", corrupted)

if decode_crc(corrupted, generator):
    print("No Error Detected")
else:
    print("Error Detected")