import re

result = 0

while True:
    try:
        input_string = input()
        numbers = re.findall(r'-?\d+', input_string)

        for number in numbers:
            try:
                int_number = int(number)
                result += int_number
            except ValueError:
                pass

    except EOFError:
        break

print(result)
