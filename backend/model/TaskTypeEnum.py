from enum import Enum
class TaskTypeEnum(Enum):
    imageRaining = 1
    videoRaining = 2

    @staticmethod
    def values():
        return list(map(lambda x: x.value, TaskTypeEnum))

    @staticmethod
    def valueOf(type):
        for item in TaskTypeEnum:
            if type == item.value:
                return item
        return None

if __name__ == "__main__":
    print(TaskTypeEnum.valueOf(1))