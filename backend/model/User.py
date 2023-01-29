from django.db import connection
from random import Random
import hashlib

def random_password(random_length=6):
    temp_password = ''
    chars = 'abcdefghijklmnopqrstuvwsyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        temp_password += chars[random.randint(0, length)]
    return temp_password

def md5(arg):
    ''' 用于把用户的密码加密 '''
    md5 = hashlib.md5()
    md5.update(bytes(arg, encoding='utf-8'))

    return md5.hexdigest()

class User:
    @staticmethod
    def test_database():
        sql = "select * from LoginInfo"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            user_info = cursor.fetchall()

        if user_info:
            print('connect database successfully!')
        else:
            print('connect database unsuccessfully!')

    @staticmethod
    def login(user_name, password):

        sql_one = "select * from LoginInfo where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql_one)
            user_info = cursor.fetchone()

        if user_info:
            if md5(password) == user_info[3]:
                sql_two = "update LoginInfo set loginState=1 where username='%s'" % user_name
                with connection.cursor() as cursor:
                    cursor.execute(sql_two)
                res = {'code': 0, 'message': 'login successfully!'}
            else:
                res = {'code': 400, 'message': 'password is not right!'}
        else:
            res = {'code': 400, 'message': 'username is not exist!'}
        print(res)
        return res

    @staticmethod
    def logout(user_name):

        sql_one = "select * from LoginInfo where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql_one)
            user_info = cursor.fetchone()

        if user_info:
            sql_two = "update LoginInfo set loginState=0 where username='%s'" % user_name
            with connection.cursor() as cursor:
                cursor.execute(sql_two)
            res = {'code': 0, 'message': 'logout successfully!'}
        else:
            res = {'code': 400, 'message': 'username is not exist!'}
        print(res)
        return res

    @staticmethod
    def isLogining(user_name):
        sql_one = "select * from LoginInfo where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql_one)
            user_info = cursor.fetchone()

        if user_info:
            if user_info[3] == 1:
                return True

        return False

    # @staticmethod
    # def getCurrentUser():
    #     sql_one = "select * from LoginInfo where loginState=1"
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_one)
    #         user_info = cursor.fetchone()
    #
    #     if user_info:
    #         return user_info[0]

    @staticmethod
    def register(user_name, password, email):
        sql = "select * from LoginInfo where username='%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql)
            user_info = cursor.fetchone()

        if user_info:
            res = {'code': 400, 'message': 'username already exists!'}
        else:
            password = md5(password)
            sql = "insert into LoginInfo (username, password, email, loginState) values ('%s', '%s', '%s', 0)" % (user_name, password, email)
            with connection.cursor() as cursor:
                cursor.execute(sql)
            res = {'code': 0, 'message': 'register successfully!'}
        print(res)
        return res

    @staticmethod
    def change_password(user_name, old_password, new_password):
        sql = "select * from LoginInfo where username='%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql)
            user_info = cursor.fetchone()

        if user_info:
            print(type(user_info))
            print(user_info[1])
            if old_password == user_info[1]:
                sql = "update LoginInfo set password = '%s' where username = '%s'" % (new_password, user_name)
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                res = {'code': 0, 'message': 'password is rights!'}
            else:
                res = {'code': 400, 'message': 'password is not right!'}
        else:
            res = {'code': 400, 'message': 'username is not exist!'}
        print(res)
        return res

    @staticmethod
    def findPassword(user_name, email):
        sql_one = "select * from LoginInfo where username='%s' and email = '%s'" % (user_name, email)
        with connection.cursor() as cursor:
            cursor.execute(sql_one)
            user_info = cursor.fetchone()

        if user_info:
            peo = user_info[0]

            temp_password = random_password(random_length=6)

            sql_two = "update LoginInfo set password='%s' where username='%s' and email = '%s'" % (md5(temp_password), user_name, email)
            with connection.cursor() as cursor:
                cursor.execute(sql_two)

            res = {'code': 0, 'message': '新密码已发送到您的邮箱'}
        else:
            res = {'code': 400, 'message': '信息不正确!'}
            temp_password = 0

        return res, temp_password



    @staticmethod
    def getUserInfo(user_name):
        sql_one = "select * from LoginInfo where username='%s'" % (user_name)
        with connection.cursor() as cursor:
            cursor.execute(sql_one)
            user_info = cursor.fetchone()

        if user_info:
            res = {'code': 200, 'data': {'username': user_info[0]}}
        else:
            res = {'code': 400, 'message': '该用户不存在'}

        return res