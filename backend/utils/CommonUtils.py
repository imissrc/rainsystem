import time
class CommonUtils:
    @staticmethod
    def getCurrentTimeStampByMilSecond():
        t = time.time()
        return int(round(t * 1000))  # 毫秒级时间戳

if __name__ == "__main__":
    print(CommonUtils.getCurrentTimeStampByMilSecond())