<template>
  <div id = "videoOCR">
    <h3>视频恢复</h3>
    <div class = "Half">
      <h4>原视频</h4>
      <div class = "video">
        <video id = "preVideo" src = "" controls = "controls" style="display: inline-block; max-width: 30vw;
      max-height: 60vh; margin: 0 12% 0;">
        </video>
      </div>
      <input type="file" accept = "video/*" id="uploadVideo" style="margin: 5% 10% 0" @change="uploadVideo($event)"/>
    </div>
    <div class = "Half">
      <h4>恢复结果</h4>
      <div class = "video">
        <video id = "resVideo" :src="this.resUrl" controls = "controls" style="display: inline-block; max-width: 30vw;
      max-height: 60vh; margin: 0 12% 0;">
        </video>
      </div>
      <button @click="videoOCR($event, 5)">文字提取</button>
    </div>
  </div>

</template>

<script>
export default {
  name: "videoOCR",
  data(){
    return{
      video:"",
      srcFileName:"",
      resUrl:"",
      resReceived:"",
    }
  },
  mounted(){
  },
  methods: {
    uploadVideo(e) {
      let videoTmp = e.target.files[0];
      if(videoTmp.size / 1024 / 1024 >= 20){
        alert('视频大小不能超过20M!')
        return;
      }
      this.video = videoTmp;
      let reader = new FileReader();
      console.log(this.video);
      reader.readAsDataURL(this.video);
      reader.onload = function () {
        document.getElementById("preVideo").src = reader.result;
      }
    },
    videoOCR(e, value){
      if(!this.video){
        alert('请先上传视频！');
        return;
      }
      let param = new FormData();
      param.append('video', this.video);
      param.append('taskType', value);
      this.$axios({
        method: 'post',
        url: '/uploadVideo',
        data: param,
        headers: {'Content-Type': 'multipart/form-data'}
      }).then(res=>{
        if(!(res.data.code === 200)){
          if(!res.data.message) {
            alert('请求失败，请重试！');
          }
          else{
            alert(res.data.message);
          }
          return;
        }
        this.srcFileName = res.data.data;
        console.log(this.srcFileName);
        var Axios = this.$axios;
        this.resReceived = false;
        var resCheck = setInterval(() => {
          let checkParam = new FormData();
          checkParam.append('video_name', this.srcFileName);
          checkParam.append('taskType', value);
          Axios({
            method: 'post',
            url: '/queryVideoTaskResult',
            data: checkParam,
            headers: {'Content-Type': 'multipart/form-data'}
          }).then(res=>{
            console.log(res);
            if((res.data.code === 200)&&(res.data.data.result === 1)&&(!this.resReceived)){
              this.resReceived = true;
              clearInterval(resCheck);
              this.resUrl = res.data.data.video;
              console.log(this.resUrl);
            }
          })
        }, 500);
      })
    },
  }
}
</script>

<style scoped>
#videoOCR{
  width: 100%;
  height: 100%;
}
.Half{
  width: 45%;
  height: 100%;
  background: ;
  margin: 10px;
  float: left;
  position: relative;
}
.video{
  width: 100%;
  min-height: 60%;
  max-height: 60%;
  float: left;
  background: ;
}
h2 {
  height: 100%;
  margin: 0;
  background: ;
  color: ;
  font-family: 楷体;
  font-size: 5em;
  letter-spacing: 8px;
  writing-mode: vertical-lr;
}

h3 {
  height: 2em;
  margin: 0;
  background: ;
  color: ;
  font-family: 楷体;
  font-size: 2em;
  vertical-align: middle;
  letter-spacing: 8px;
}
h4{
  font-family: 楷体;
  font-size: 1.5em;
}
button {
  width: 18%;
  margin: 5% 10% 0;
  font-family: 楷体;
  font-size: 1.2em;
  border-radius: 10%;
  background-color: ;
  color: #2c3e50;
}
</style>

<style>
html,body,#videoOCR {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  width: 100%;
  height: 100%;
  margin: 5px 0 0 0;
  padding: 0;
  overflow: hidden;
  background: url("../.././assets/bg.jpg") repeat;
  background-size: cover;
}
</style>
