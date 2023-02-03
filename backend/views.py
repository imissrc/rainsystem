import uuid
import rainsystem.settings as settings
import time
import backend.deal_derain as deal_derain
from backend.livenvr import upload_video_livenvr
from backend.ImageVideo import mp4ToAvi, videoMerge
import backend.text_spot as textspot

from backend.dao.UserInfoDAO import UserInfoDAO
# from backend.Files import Files
from django.conf import settings
from django.core.mail import send_mail
# from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.http import JsonResponse
import json
import os
from backend.model.TaskTypeEnum import TaskTypeEnum
from backend.model.TaskHistoryDetail import TaskHistoryDetail
from backend.dao.TaskHistoryDAO import TaskHistoryDAO
from backend.dao.TaskHistoryDetailDAO import TaskHistoryDetailDAO

UserInfoDAO.test_database()
# currentUserName = User.getCurrentUser()

cur_path = os.path.abspath('.')
#import backend.textspot.mmocr.init_text_model as InitTextModel


def login(request):
    if request.method == 'POST':
        userinfo = json.loads(request.body)
        username = userinfo['username']
        password = userinfo['password']
        res = UserInfoDAO.login(user_name=username, password=password)
        return JsonResponse(res, safe=False)

def getLoginState(request):
    if request.method == 'GET':
        username = request.GET['username']
        res = UserInfoDAO.getLoginState(user_name=username)
        return JsonResponse(res, safe=False)

def logout(request):
    if request.method == 'GET':
        username = request.GET['username']
        res = UserInfoDAO.logout(username)
        return JsonResponse(res, safe=False)

def register(request):
    if request.method == 'POST':
        userinfo = json.loads(request.body)
        username = userinfo['username']
        email = userinfo['email']
        password = userinfo['password']
        res = UserInfoDAO.register(user_name=username, password=password, email=email)

        return JsonResponse(res, safe=False)

def findPassword(request):
    if request.method == 'POST':
        userinfo = json.loads(request.body)
        username = userinfo['username']
        email = userinfo['email']

        res, temp_password = UserInfoDAO.findPassword(username, email)

        if res['code'] == 0:
            send_mail('亲爱的用户'+username+'我们给你生成了一个随机的6位密码，请尽快登录修改你的密码吧', temp_password, 'imissrc@163.com', [email])

        return JsonResponse(res, safe=False)


def changePassword(request):
    if request.method == 'POST':
        userinfo = json.loads(request.body)
        username = userinfo['username']
        oldPassward = userinfo['oldPassword']
        newPassward1 = userinfo['newPassword1']

        res = UserInfoDAO.change_password(user_name=username, old_password=oldPassward, new_password=newPassward1)

        return JsonResponse(res, safe=False)

def getUserInfo(request):
    if request.method == 'GET':
        userinfo = json.loads(request.body)
        username = userinfo['username']

        res = UserInfoDAO.getUserInfo(user_name=username)

        return JsonResponse(res, safe=False)

'''
根据taskType，运行对应的模型
'''


def runModel(taskType, file_path, file_type):
    print("taskType:" + str(taskType))
    if (file_type == 0):
        if (taskType == 1):
            # deraining
            deal_derain.getImageDerain(settings.derain_moss_model, file_path, file_path.replace("input", "output"), 'moss')

        elif (taskType == 3):
            # deblurring
            pass

        elif (taskType == 5):
            # textdetect
            img = file_path
            output = file_path.replace('input', 'output')
            export = output  # 每张图片的结果 导出的文件夹路径
            settings.mmocr_model.readtext(img=img, output=output, export=export)   # 直接写文件
            pass
    elif (file_type == 1):
        if (taskType == 1):
            # deraining
            deal_derain.getVideoDerain(settings.derain_moss_model, file_path, file_path.replace("input", "output"), 'moss')
        elif (taskType == 3):
            # deblurring
            pass
        elif (taskType == 5):
            # textdetect
            textspot.get_video_ocr(settings.mmocr_model, file_path, file_path.replace("input", "output"))
        elif (taskType == 6):
            # derain then textdetect
            input_video_images, output_video_images, fps = deal_derain.runVideoDerainModel(settings.derain_moss_model, file_path, 'moss')
            out_images = textspot.get_img_list_ocr(settings.mmocr_model, output_video_images)
            videoMerge(input_video_images, out_images, fps, file_path.replace('input', 'output'))
    else:
        #error
        pass


def uploadImagesAndRestore(request):
    if request.method == 'POST':
        username = request.POST['username']
        taskType = int(request.POST['taskType'])
        imageList = request.FILES.getlist('images', [])
        if len(imageList) == 0:
            return JsonResponse({"code": 400, "message": "upload list can not be empty"}, safe=False)

        taskTypeEnum = TaskTypeEnum.valueOf(taskType)
        if taskTypeEnum is None:
            return JsonResponse({"code": 400, "message": "未知的图像处理任务"}, safe=False)

        imageUrlList = []
        for image in imageList:
            ext = image.name.split('.')[-1]
            image_name = 'input-' + generateFileName(ext, settings.MEDIA_ROOT)
            if image_name == 'input-':
                res = {"code": 400, "message": "图片上传失败，请重试"}
                return JsonResponse(res, safe=False)

            # 根据任务类型将输入图片存到相应目录中
            image_path = generateFilePath(taskTypeEnum, image_name)
            # print(image_path)
            with open(image_path, 'wb') as f:
                for chunk in image.chunks():
                    f.write(chunk)
            f.close()
            imageUrlList.append(getResourceUrl(taskTypeEnum, image_name))

        taskHistoryId = TaskHistoryDAO.addTaskHistory(username, taskType)
        print('imageUrlList: ')
        print(imageUrlList)
        TaskHistoryDetailDAO.addTaskHistoryDetail(buildTaskHistoryDetailList(taskHistoryId, imageUrlList))
        #todo 异步执行去雨任务
        res = {"code": 200, "data": {'taskHistoryId': taskHistoryId, 'total': len(imageList)}}
        print(res)
        return JsonResponse(res, safe=False)
    else:
        print(request.method)
        return JsonResponse({"code": 400, "message": "error"}, safe=False)

def buildTaskHistoryDetailList(taskHistoryId, resourceUrlList):
    taskHistoryDetailList = []
    for resourceUrl in resourceUrlList:
        taskHistoryDetail = TaskHistoryDetail(taskHistoryId, resourceUrl, '')
        taskHistoryDetailList.append(taskHistoryDetail)
    return taskHistoryDetailList

def getDetailByTaskHistoryId(request):
    if request.method == 'GET':
        taskHistoryId = int(request.GET.get('taskHistoryId'))
        start = int(request.GET.get('start'))
        pageSize = int(request.GET.get('pageSize'))
        res = TaskHistoryDetailDAO.getDetailByTaskHistoryId(taskHistoryId, start, pageSize)
        return JsonResponse(res, safe=False)

def uploadVideo(request):
    if request.method == 'POST':
        video = request.FILES.get('video', None)

        ext = video.name.split('.')[-1]
        video_name = generateFileName(ext, settings.MEDIA_ROOT)
        if video_name == '':
            res = {"code": 400, "message": "视频上传失败，请重试"}
            return JsonResponse(res, safe=False)
        # 根据任务类型将输入图片存到相应目录中
        video_path = generateFilePath(0, 'input-' + video_name)
        # print(image_path)
        with open(video_path, 'wb') as f:
            for chunk in video.chunks():
                f.write(chunk)
        f.close()
        if ext != 'avi':
            res_path = video_path.replace(video_path.split('.')[-1], 'avi')
            mp4ToAvi(video_path, res_path)
        input_video_name = 'input-' + video_name.replace(video_path.split('.')[-1], 'avi')
        print(input_video_name)
        # input_video_path = settings.RESOURCE_HOST + '/' + settings.MODEL_DIRECTORY[0] + '/' + input_video_name
        # input_res_url = upload_video_livenvr(input_video_path, 1,
        #                                      host=settings.HOST, user_name=settings.USER, password=settings.PASSWORD)
        # if input_res_url != ' ':
        #     src_display_url = settings.HOST + "/play.html?channel=" + str(settings.CHANNELS_SRC[0]) + "&iframe=yes"
        res = {"code": 200, "message": "success", "data": {'name':video_name}}

        return JsonResponse(res, safe=False)
    else:
        print(request.method)
        return JsonResponse({"code": 400, "message": "error"}, safe=False)


def runVideo(request):
    if request.method == 'POST':
        video_name = request.POST['video']
        taskType = int(request.POST['taskType'])
        if not (taskType >= 1 and taskType <= 7):
            return JsonResponse({"code": 400, "message": "未知的图像处理任务"}, safe=False)
        video_path = generateFilePath(taskType, 'input-' + video_name)
        print(video_path)
        os.system("cp -f " + generateFilePath(0, 'input-' + video_name) + " " + video_path)
        runModel(taskType, video_path, 1)
        res = {"code": 200, "message": "success"}
        return JsonResponse(res, safe=False)

def getFiles(path, suffix):
    # 文件查找
    return [os.path.join(root, file) for root, dirs, files in os.walk(path) for file in files if file.endswith(suffix)]


def queryImageTaskResult(request):
    if request.method == 'POST':

        image_name = request.POST['image_name']
        taskType = int(request.POST['taskType'])
        output_image_name = "output-" + image_name

        image_path = generateFilePath(taskType, output_image_name)
        # print(image_path.replace('/input-' + image_name, ''))
        results = getFiles(image_path.replace("output-" + image_name, ''), output_image_name)
        if len(results) == 0:
            time.sleep(1)
            res = {"code": 200, "message": "success",
                   "data": {"result": 0}}
            return JsonResponse(res, safe=False)
            # 查找output-xxx.jpg文件是否在目录中，是则返回路径
        else:
            url_prefix = request.build_absolute_uri('/')
            url_file = os.path.join(url_prefix, results[0][2:].replace('\\','/')) #todo: url地址格式不正确
            res = {"code": 200, "message": "success",
                   "data": {"result": 1,"image":url_file}}
            return JsonResponse(res, safe=False)
    else:
        print(request.method)
        return JsonResponse({"code": 400, "message": "error"}, safe=False)

def queryVideoTaskResult(request):
    if request.method == 'POST':
        video_name = request.POST['video_name']
        res_video_name = video_name.replace(video_name.split('.')[-1], 'avi')
        taskType = int(request.POST['taskType'])
        output_video_name = "output-" + res_video_name
        url_prefix = request.build_absolute_uri('/')
        output_video_path = settings.RESOURCE_HOST + "/" + settings.MODEL_DIRECTORY[taskType] + "/" + output_video_name
        print(output_video_path)
        output_res_url = upload_video_livenvr(output_video_path, settings.CHANNELS_RES[taskType],
                                              host=settings.HOST, user_name=settings.USER, password=settings.PASSWORD)
        if output_res_url == ' ':
            time.sleep(1)
            res = {"code": 200, "message": "success",
                   "data": {"result": 0}}
            return JsonResponse(res, safe=False)
            # 查找output-xxx.jpg文件是否在目录中，是则返回路径
        else:
            res_display_url = settings.HOST + "/play.html?channel=" + str(settings.CHANNELS_RES[taskType]) + "&iframe=yes"
            #print(res_display_url)
            res = {"code": 200, "message": "success",
                   "data": {"result": 1, "resVideo":res_display_url}}
            return JsonResponse(res, safe=False)
    else:
        print(request.method)
        return JsonResponse({"code": 400, "message": "error"}, safe=False)



def generateFilePath(taskTypeEnum, image_name):
    directory_path = os.path.join(settings.RESOURCE_ROOT, taskTypeEnum.name)
    print("directory_path: " + directory_path)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return os.path.join(settings.RESOURCE_ROOT, taskTypeEnum.name, image_name)


def generateFileName(ext, filePath):
    count = 5
    i = 0
    while i < count:
        imageName = str(uuid.uuid1()) + "." + ext
        imagePath = os.path.join(filePath, imageName)
        if not os.path.exists(imagePath):
            return imageName
        i += 1
    return ''


def getResourceUrl(taskTypeEnum, resouceName):
    return os.path.join(settings.RESOURCE_IP_PORT, settings.RESOURCE_RELATIVE_PATH, taskTypeEnum.name,
                                    resouceName.replace('\\', '/'))