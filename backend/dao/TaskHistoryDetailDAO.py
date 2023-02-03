import json

from django.db import connection
from backend.model.TaskHistoryDetail import TaskHistoryDetail

class TaskHistoryDetailDAO:
    @staticmethod
    def getDetailByTaskHistoryId(taskHistoryId, start, pageSize):
        sqlOne = "select * from task_history_detail where taskHistoryId = %s limit %s, %s"
        with connection.cursor() as cursor:
            cursor.execute(sqlOne, (taskHistoryId, start, pageSize))
            taskHistoryDetailInfo = cursor.fetchall()

        detailList = []
        if taskHistoryDetailInfo:
            for item in taskHistoryDetailInfo:
                taskHistoryDetail = TaskHistoryDetail(item[1], item[3], item[2])
                detailList.append(taskHistoryDetail.keys())
            res = {'code': 200, 'data': detailList}
        else:
            res = {'code': 400, 'message': 'detail is not exist!'}
        print(res)
        return res

    @staticmethod
    def addTaskHistoryDetail(taskHistoryDetailList):
        if taskHistoryDetailList == []:
            return
        taskHistoryDetailListInDb = []
        for item in taskHistoryDetailList:
            taskHistoryDetailListInDb.append((item.taskHistoryId[0], item.originUrl[0]))
        sql_one = "insert into task_history_detail (taskHistoryId, originUrl) values (%s, %s)"
        with connection.cursor() as cursor:
            cursor.executemany(sql_one, taskHistoryDetailListInDb)