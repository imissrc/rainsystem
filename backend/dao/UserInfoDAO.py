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

class UserInfoDAO:
    @staticmethod
    def test_database():
        sql = "select * from user_info"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            user_info = cursor.fetchall()

        if user_info:
            print('connect database successfully!')
        else:
            print('connect database unsuccessfully!')

    @staticmethod
    def login(user_name, password):

        sql_one = "select * from user_info where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql_one)
            userInfo = cursor.fetchone()

        if userInfo:
            if md5(password) == userInfo[3]:
                sql_two = "update user_info set loginState=1 where username='%s'" % user_name
                with connection.cursor() as cursor:
                    cursor.execute(sql_two)
                res = {'code': 200, 'message': 'login successfully!'}
            else:
                res = {'code': 400, 'message': 'password is not right!'}
        else:
            res = {'code': 400, 'message': 'username is not exist!'}
        print(res)
        return res

    @staticmethod
    def logout(user_name):

        sqlOne = "select * from user_info where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sqlOne)
            userInfo = cursor.fetchone()

        if userInfo:
            sql_two = "update user_info set loginState = 0 where username='%s'" % user_name
            with connection.cursor() as cursor:
                cursor.execute(sql_two)
            res = {'code': 200, 'message': 'logout successfully!'}
        else:
            res = {'code': 400, 'message': 'username is not exist!'}
        print(res)
        return res

    @staticmethod
    def getLoginState(user_name):
        sql = "select * from user_info where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql)
            userInfo = cursor.fetchone()

        if userInfo:
            if userInfo[3] == 1:
                res = {'code': 200, 'data': True}
            else:
                res = {'code': 200, 'data': False}
        else:
            res = {'code': 400, 'message': False}
        print(res)
        return res

    # @staticmethod
    # def getCurrentUser():
    #     sql_one = "select * from user_info where loginState=1"
    #     with connection.cursor() as cursor:
    #         cursor.execute(sql_one)
    #         user_info = cursor.fetchone()
    #
    #     if user_info:
    #         return user_info[0]

    @staticmethod
    def register(username, password, email):
        sql = "select * from user_info where username='%s'" % username
        with connection.cursor() as cursor:
            cursor.execute(sql)
            userInfo = cursor.fetchone()

        if userInfo:
            res = {'code': 400, 'message': 'username already exists!'}
        else:
            password = md5(password)
            sql = "insert into user_info (username, password, email, loginState) values ('%s', '%s', '%s', 0)" % (username, password, email)
            with connection.cursor() as cursor:
                cursor.execute(sql)
            res = {'code': 200, 'message': 'register successfully!'}
        print(res)
        return res

    @staticmethod
    def change_password(user_name, old_password, new_password):
        sql = "select * from user_info where username='%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql)
            userInfo = cursor.fetchone()

        if userInfo:
            if old_password == userInfo[1]:
                sql = "update userInfo set password = '%s' where username = '%s'" % (new_password, user_name)
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                res = {'code': 200, 'message': 'password is rights!'}
            else:
                res = {'code': 400, 'message': 'password is not right!'}
        else:
            res = {'code': 400, 'message': 'username is not exist!'}
        print(res)
        return res

    @staticmethod
    def findPassword(username, email):
        sqlOne = "select * from user_info where username='%s' and email = '%s'" % (username, email)
        with connection.cursor() as cursor:
            cursor.execute(sqlOne)
            userInfo = cursor.fetchone()

        if userInfo:
            temp_password = random_password(random_length=6)

            sqlTwo = "update user_info set password='%s' where username='%s' and email = '%s'" % (md5(temp_password), username, email)
            with connection.cursor() as cursor:
                cursor.execute(sqlTwo)

            res = {'code': 200, 'message': '新密码已发送到您的邮箱'}
        else:
            res = {'code': 400, 'message': '信息不正确!'}
            temp_password = 0

        return res, temp_password