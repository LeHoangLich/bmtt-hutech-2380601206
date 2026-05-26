def tao_tuple_tu_list(lst):
    return tuple(lst)

input_list = input("Nhập danh sách các số, cách nhau bằng dấu phẩy: ")
numbers = list(map(input, input_list.split(',')))

my_tuple = tao_tuple_tu_list(numbers)
print("ListL ", numbers)
print("Tuple từ List: ", my_tuple)