# value= "ac"
# values = ["ac", 'db']
# keys = [[1],[3],[5]]
# key = 2
# #print('' < str("abc"))
# for i in range(len(values)):
#     if (value < values[i]):
#         print("12", values[:i], values[i:])
#         values = values[:i] + [value] + values[i:]
#         keys = keys[:i] + [[key]] + keys[i:]
#         break
#     elif (i + 1 == len(values)):
#         values.append(value)
#         keys.append([key])
#         break
# print(values)
# print(keys)
import math
print(3 / 2 - 1)

a = [1,2,3,4,5]
print(a[3:])
print(a[:3])
del a[3]
print(a)
a = [1,2]
if not (a == tuple):
    print("튜플이 아님")
