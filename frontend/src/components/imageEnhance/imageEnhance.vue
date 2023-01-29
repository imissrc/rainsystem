<template>
  <div>
<!--    <div style="margin-top: 0px; margin-left: -8px; margin-right: -8px">-->
<!--      <el-menu-->
<!--        :default-active="activeIndex"-->
<!--        class="el-menu-demo"-->
<!--        mode="horizontal"-->
<!--        @select="handleSelect"-->
<!--        background-color="#545c64"-->
<!--        text-color="#fff"-->
<!--        active-text-color="#ffd04b"-->
<!--      >-->
<!--        <el-menu-item index="imageEnhance">图像恢复</el-menu-item>-->
<!--        <el-menu-item index="videoEnhance">视频恢复</el-menu-item>-->
<!--        <el-menu-item index="imageOCR">图像文字检测</el-menu-item>-->
<!--        <el-menu-item index="videoOCR">视频文字检测</el-menu-item>-->
<!--&lt;!&ndash;        <el-menu-item index="runPredict">运行</el-menu-item>&ndash;&gt;-->
<!--&lt;!&ndash;        <el-menu-item index="stopPredict">停止运行</el-menu-item>&ndash;&gt;-->
<!--&lt;!&ndash;        <el-menu-item index="exportTable" :loading="exportLoading">导出</el-menu-item>&ndash;&gt;-->
<!--&lt;!&ndash;        <el-menu-item>&ndash;&gt;-->
<!--&lt;!&ndash;          <el-tag&ndash;&gt;-->
<!--&lt;!&ndash;            size="medium"&ndash;&gt;-->
<!--&lt;!&ndash;            :type="taskStatus | statusFilter"&ndash;&gt;-->
<!--&lt;!&ndash;          >{{ statusOptions[taskStatus] }}&ndash;&gt;-->
<!--&lt;!&ndash;          </el-tag>&ndash;&gt;-->
<!--&lt;!&ndash;        </el-menu-item>&ndash;&gt;-->
<!--&lt;!&ndash;        <el-menu-item>&ndash;&gt;-->
<!--&lt;!&ndash;          <el-tag&ndash;&gt;-->
<!--&lt;!&ndash;            size="medium"&ndash;&gt;-->
<!--&lt;!&ndash;          >准确率：{{ accuracy }}&ndash;&gt;-->
<!--&lt;!&ndash;          </el-tag>&ndash;&gt;-->
<!--&lt;!&ndash;        </el-menu-item>&ndash;&gt;-->
<!--      </el-menu>-->
<!--    </div>-->
    <div id = "imageEnhance">
      <h3>图片恢复</h3>
      <div class = "Half">
        <h4>原图片</h4>
        <div class = "img"><img id = "preImg" style="display: inline-block; max-width: 30vw;
        max-height: 60vh; margin: 0 12% 0;" src="" alt="">
        </div>
        <input type="file" accept = "image/*" id="uploadImg" style="margin: 5% 10% 0" @change="uploadImg($event)"/>
      </div>
      <div class = "Half">
        <h4>恢复结果</h4>
        <div class = "img"><img id = "enhancedImg" style="display: inline-block; max-width: 30vw;
        max-height: 60vh; margin: 0 12% 0;" v-if = "this.resUrl" :src="this.resUrl" alt="">
        </div>
        <button @click="imgEnhance($event, 1)">去雨</button>
        <button @click="imgEnhance($event, 2)">去雾</button>
        <button @click="imgEnhance($event, 3)">去模糊</button>
        <button @click="imgEnhance($event, 4)">色彩增强</button>
      </div>
  </div>

  </div>

</template>

<script>
export default {
  name: "imageEnhance",
  data(){
    return{
      img:"",
      srcFileName:"",
      resUrl:"",
      resReceived:"",
      activeIndex: 'imageEnhance',
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
    imgEnhance(e, value){
      if(!this.img){
        alert('请先上传图片！');
        return;
      }
      console.log(this.img);
      let param = new FormData();
      param.append('image', this.img);
      param.append('taskType', value);
      this.instance.post('/uploadImage',param
      ).then((res)=>{
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
        var Axios = this.instance;
        this.resReceived = false;
        var resCheck = setInterval(() => {
          let checkParam = new FormData();
          checkParam.append('image_name', this.srcFileName);
          checkParam.append('taskType', value);
          Axios.post('/queryImageTaskResult', checkParam,
          ).then((res)=>{
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

    handleSelect (key) {
      if (key === 'home') {
        this.$router.push(`/home/`)
      } else if (key === 'importFile') {
        this.openImportDialog()
      } else if (key === 'runPredict') {
        this.runPredict()
      } else if (key === 'stopPredict') {
        this.stopPredict()
      } else if (key === 'manual') {
        this.openManualDialog()
      } else if (key === 'history') {
        this.$router.push(`/history/`)
      } else if (key === 'saveHistory') {
        this.storeHistory()
      } else if (key === 'exportTable') {
        this.exportData()
      } else if (key === 'logout') {
        this.logout()
      } else if (key === 'changePassword') {
        this.changeVisible = true
      }
    },
  }
}
</script>

<style scoped>
#imageEnhance{
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
html,body,#imageEnhance {
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
