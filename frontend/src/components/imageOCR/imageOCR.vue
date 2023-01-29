<template>
  <div id = "imageOCR">
    <h3>图片文字提取</h3>
    <div class = "Half">
      <h4>原图片</h4>
      <div class = "img"><img id = "preImg" style="display: inline-block; max-width: 30vw;
      max-height: 60vh; margin: 0 12% 0;" src="" alt="">
      </div>
      <input type="file" accept = "image/*" id="uploadImg" style="margin: 5% 10% 0" @change="uploadImg($event)"/>
    </div>
    <div class = "Half">
      <h4>文字提取结果</h4>
      <div class = "img"><img id = "resImg" style="display: inline-block; max-width: 30vw;
      max-height: 60vh; margin: 0 12% 0;" v-if = "this.resUrl" :src="this.resUrl" alt="">
      </div>
      <button @click="imgOCR($event, 5)">文字提取</button>
    </div>
  </div>

</template>

<script>
export default {
  name: "imageOCR",
  data(){
    return{
      img:"",
      srcFileName:"",
      resUrl:"",
      resReceived:"",
    }
  },
  methods: {
    uploadImg(e) {
      let imgTmp = e.target.files[0];
      if(imgTmp.size / 1024 / 1024 >= 4){
        alert('图片大小不能超过4M!')
        return;
      }
      this.img = imgTmp;
      let reader = new FileReader();
      reader.readAsDataURL(this.img);
      reader.onload = function () {
        document.getElementById("preImg").src = reader.result;
      }
    },
    imgOCR(e, value){
      if(!this.img){
        alert('请先上传图片！');
        return;
      }
      let param = new FormData();
      param.append('image', this.img);
      param.append('taskType', value);
      this.$axios({
        method: 'post',
        url: '/uploadImage',
        data: param,
        headers: {'Content-Type': 'multipart/form-data'}
      }).then((res)=>{
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
          checkParam.append('image_name', this.srcFileName);
          checkParam.append('taskType', value);
          Axios({
            method: 'post',
            url: '/queryImageTaskResult',
            data: checkParam,
            headers: {'Content-Type': 'multipart/form-data'}
          }).then((res)=>{
            console.log(res);
            if((res.data.code === 200)&&(res.data.data.result === 1)&&(!this.resReceived)){
              this.resReceived = true;
              clearInterval(resCheck);
              this.resUrl = res.data.data.image;
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
#imageOCR{
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
.img{
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
html,body,#imageOCR {
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
