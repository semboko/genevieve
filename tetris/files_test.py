file = open("./explosion.wav", "rb")

content = file.read(30)
print(content)

file.close()


file2 = open("./test_writing.txt", "w")
file2.write("Some content")
file2.close()


with open("./test_writing2.txt", "w") as file3:
    file3.write("Some content")
