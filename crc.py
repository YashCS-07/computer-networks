"""
CRC (Cyclic Redundancy Check)

Features:
- CRC Encoding
- CRC Decoding
- Input Validation
- Automatic Error Demonstration
"""

from typing import Tuple


def xor(a: str, b: str) -> str:
    """
    Perform XOR between two binary strings
    (ignoring the first bit as required in CRC division).
    """
    return ''.join(
        '0' if a[i] == b[i] else '1'
        for i in range(1, len(b))
    )


def validate_binary(bits: str, name: str) -> None:
    """
    Validate binary input.
    """
    if not bits:
        raise ValueError(f"{name} cannot be empty.")

    if any(bit not in "01" for bit in bits):
        raise ValueError(f"{name} must contain only 0 and 1.")

    if name == "Generator":
        if bits[0] != "1":
            raise ValueError("Generator polynomial must start with 1.")
        if len(bits) < 2:
            raise ValueError("Generator must contain at least two bits.")


def mod2div(dividend: str, divisor: str) -> str:
    """
    Perform Modulo-2 Division and return the CRC remainder.
    """
    pick = len(divisor)
    temp = dividend[:pick]

    while pick < len(dividend):

        if temp[0] == "1":
            temp = xor(divisor, temp) + dividend[pick]
        else:
            temp = xor("0" * pick, temp) + dividend[pick]

        pick += 1

    # Final division
    if temp[0] == "1":
        temp = xor(divisor, temp)
    else:
        temp = xor("0" * pick, temp)

    return temp


def encode_crc(data: str, generator: str) -> Tuple[str, str]:
    """
    Generate CRC remainder and codeword.
    """
    validate_binary(data, "Data")
    validate_binary(generator, "Generator")

    appended_data = data + "0" * (len(generator) - 1)

    remainder = mod2div(appended_data, generator)

    codeword = data + remainder

    return remainder, codeword


def decode_crc(codeword: str, generator: str) -> bool:
    """
    Return True if no error is detected.
    """
    validate_binary(codeword, "Codeword")
    validate_binary(generator, "Generator")

    remainder = mod2div(codeword, generator)

    return '1' not in remainder


def introduce_error(codeword: str, position: int) -> str:
    """
    Flip one bit of the codeword.
    """
    if not (0 <= position < len(codeword)):
        raise IndexError("Bit position out of range.")

    corrupted = list(codeword)

    corrupted[position] = (
        '1' if corrupted[position] == '0' else '0'
    )

    return ''.join(corrupted)


def main() -> None:

    print("=" * 50)
    print("        CRC (Cyclic Redundancy Check)")
    print("=" * 50)

    try:

        data = input("Enter Data Bits      : ").strip()
        generator = input("Enter Generator Bits : ").strip()

        remainder, codeword = encode_crc(data, generator)

        print("\n----------- Sender Side -----------")
        print(f"Original Data      : {data}")
        print(f"CRC Remainder      : {remainder}")
        print(f"Generated Codeword : {codeword}")

        print("\n----------- Receiver Side -----------")

        received = input(
            "Enter Received Codeword (Press Enter to use original): "
        ).strip()

        if not received:
            received = codeword

        if decode_crc(received, generator):
            print("Result : No Error Detected")
        else:
            print("Result : Error Detected")

        print("\n------ Automatic Error Demonstration ------")

        position = len(codeword) // 2

        corrupted = introduce_error(codeword, position)

        print(f"Bit Flipped Position : {position}")
        print(f"Corrupted Codeword   : {corrupted}")

        if decode_crc(corrupted, generator):
            print("Result : No Error Detected")
        else:
            print("Result : Error Detected")

    except ValueError as e:
        print("\nInput Error:", e)

    except Exception as e:
        print("\nUnexpected Error:", e)


if __name__ == "__main__":
    main()