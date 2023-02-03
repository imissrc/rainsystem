import json
from backend.model.TaskHistoryDetail import TaskHistoryDetail
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TaskHistoryDetail):
            return {'taskHistoryId': ''}
        else:
            return super(MyEncoder, self).default(obj)