class TaskHistoryDetail:
    def __init__(self, taskHistoryId, originUrl, targetUrl):
        self.taskHistoryId = taskHistoryId,
        self.originUrl = originUrl,
        self.targetUrl = targetUrl

    def keys(self):
        return {'taskHistoryId': self.taskHistoryId, 'originUrl': self.originUrl, 'targetUrl': self.targetUrl}
