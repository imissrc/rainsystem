from django.db import connection
from backend.utils.CommonUtils import CommonUtils

class TaskHistoryDAO:
    @staticmethod
    def addTaskHistory(username, taskType):

        sqlOne = "insert into task_history (username, taskType, timestamp) values ('%s', '%d', '%d')" \
                  % (username, taskType, CommonUtils.getCurrentTimeStampByMilSecond())
        with connection.cursor() as cursor:
            cursor.execute(sqlOne)

        sqlTwo = "select id from task_history where username = '%s' order by timestamp desc limit 1" % username
        with connection.cursor() as cursor:
            cursor.execute(sqlTwo)
            info = cursor.fetchone()
        taskHistoryId = None
        if info is not None:
            taskHistoryId = info[0]
        return taskHistoryId
