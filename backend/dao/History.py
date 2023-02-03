from django.db import connection

class History:

    @staticmethod
    def getUserHistory(user_name):

        sql = "select * from history where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql)
            user_history = cursor.fetchall()

        if user_history:
            historyList=[]
            for history in user_history:
                historyList.append(history[1])
            res = {'code': 0, 'historyList': historyList, 'total': len(historyList)}
        else:
            res = {'code': 0, 'historyList': '', 'total': 0}
        print(res)
        return res

    @staticmethod
    def getUserHistoryCount(user_name):
        sql = "select count(*) from history where username = '%s'" % user_name
        with connection.cursor() as cursor:
            cursor.execute(sql)
            user_history_count = cursor.fetchone()
        return user_history_count[0]

    @staticmethod
    def addUserHistory(user_name, title):
        sql = "insert into history (username, title) values ('%s', '%s')" % (user_name, title)
        with connection.cursor() as cursor:
            cursor.execute(sql)

    @staticmethod
    def deleteUserHistory(user_name, file_name):
        sql = "delete from history where username = '%s' and title = '%s'" % (user_name, file_name)
        with connection.cursor() as cursor:
            cursor.execute(sql)