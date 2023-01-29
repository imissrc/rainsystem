图像增强任务demo版

前端使用vue搭建，后端使用django搭建

目前已实现任务：图像去雾、图像去雨、图像文字检测
待实现任务：图像去模糊、图像色彩增强

前端固定的后端接口为：10.109.246.55：8070，如需改变，请修改VUE.CONFIG.JS文件

后端需求：python3.6+ pytorch1.8+ 
启动指令：CUDA_VISIBLE_DEVICES=1 python manage.py runserver 0.0.0.0:8070
CUDAid与端口可根据需求自行调整

后端任务所使用的深度学习模型在backend目录下，如有需求可更换其他预训练好的模型

后端视频处理需要启动livenvr服务，目前该服务安装于10.109.246.55的docker中，
name为docker-livenvr，使用前请检查该docker是否处于运行中（docker ps）
可能需自行启动（docker start docker-livenvr）
 livenvr开发接口文档：https://nvr.liveqing.com:10810/apidoc/