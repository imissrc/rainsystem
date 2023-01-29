import json
import requests
import hashlib
def upload_video_livenvr(videoUrl, channel, host = "http://10.109.246.55:10800",
                         user_name = 'admin', password = 'admin'):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    login_params = {'username':user_name, 'password':m.hexdigest()}
    set_params = {'Channel':channel, 'Name': 'Channel' + str(channel), 'Protocol':'FILE','RTSP':videoUrl,
                  'OnDemand':'1','Transport':'TCP', 'Enable':'1', 'token': ''}
    check_params = {'channel':channel, 'token': ''}
    res_url = ' '
    response = requests.get(host + "/api/v1/login", params = login_params)
    stat = json.loads(response.text).get('LiveQing').get('Header').get('ErrorNum')
    if stat != '200':
        print(json.loads(response.text).get('LiveQing').get('Header').get('ErrorString'))
    else:
        print("login success!")
        URLToken = json.loads(response.text).get('LiveQing').get('Body').get('URLToken')
        set_params['token'] = URLToken
        response = requests.get(host + "/api/v1/setchannelconfig", params = set_params)
        stat = json.loads(response.text).get('LiveQing').get('Header').get('ErrorNum')
        if stat != '200':
            print(json.loads(response.text).get('LiveQing').get('Header').get('ErrorString'))
        else:
            print("config setted.")
            stat = ''
            while stat != '200':
                check_params['token'] = URLToken
                response = requests.get(host + "/api/v1/getchannelstream",
                                        params = check_params)
                stat = json.loads(response.text).get('LiveQing').get('Header').get('ErrorNum')
            res_url = (json.loads(response.text).get('LiveQing').get('Body').get('URL'))
    return res_url
if __name__ == "__main__":
    videoUrl = "http://10.109.246.55:9000/out.avi"
    upload_video_livenvr(videoUrl, 2)