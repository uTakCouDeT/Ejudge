import sys

input_file_name = sys.argv[1]
output_file_name = sys.argv[2]

result = 0

with open(input_file_name, 'r') as input_file:
    for line in input_file:
        try:
            num = int(line)
            result += num
        except ValueError:
            pass

with open(output_file_name, 'w') as output_file:
    output_file.write(str(result % 256))
