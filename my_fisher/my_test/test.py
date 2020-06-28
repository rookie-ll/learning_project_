def lv(lv):
    def fun(f):
        def fun2(a, b):
            print("我是个装饰器")
            print(a + b)
            print(lv)
            return f(a, b)

        return fun2

    return fun


@lv(1)
def test(a, b):
    print("hello")
    return "hello"


# my_test(1, 2)


def hello():
    i = 1
    while True:
        yield i
        i += 1


# s = hello()
# print(s)
# print(next(s))
# print(next(s))
# print(next(hello()))
# print(next(hello()))
# for a in range(3):
#     print(next(hello()))

# x = [i for i in range(2)]
# print(x)


# class Iter(object):
#     def __init__(self):
#         self.i = 0
#
#     def __iter__(self):
#         return self
#
#     def __next__(self):
#         self.i += 1
#         return self.i
#
#
# a = Iter()
# print(next(a))
# print(next(a))
# print(next(a))
# ls = [2, 4, 6]
#
#
# def fun(n):
#     print("函数内部")
#     return n % 2==1
#
#
# nls = filter(fun, ls)
# # print('e')
# # print(list(nls))
# a=set(ls)
# for i in a:
#     print(i)
#
# a=set()
# print(a)
# b=list()
# print(b)
# ls=[1,2,3,4,5]
# def fun(n):
#     return n%2==0
#
# s=map(fun,ls)
# b=filter(fun,ls)
#
# print(list(s))
# print(list(b))

# class A():
#     def __init__(self):
#         self.d=[1,2,3,4]
#
#     def __getitem__(self, item):
#         return self.d[item]
#
# for i in A():
#     print(i)

