<template>
  <el-card class="box-card imageEnhance">
    <!--    <div slot="header" class="clearfix" style="position: relative; left: -8%">-->
    <!--      <span>图像{{ name }}</span>-->
    <!--    </div>-->
    <div class="leftArea">
      <el-col :span="11">
        <el-row>
          原图片
        </el-row>
        <el-row>
          <el-card class="box-card display-image">
            <el-image :src="originUrl" />
          </el-card>
        </el-row>
        <el-row>
          <el-upload
            ref="uploadImage"
            class="upload-image"
            :auto-upload="false"
            action="#"
            multiple
            accept="image/jpeg,image/png"
            :show-file-list="false"
            :on-change="handleChange"
          >
            <el-button slot="trigger" size="small" type="primary">选取文件</el-button>
            <el-button style="margin-left: 10px;" size="small" type="success" @click="uploadImgAndRestore">上传并开始图像{{ name }}</el-button>
            <div slot="tip" class="el-upload__tip">只能上传jpg/png文件，且不超过500kb</div>
            <div v-show="showUploadImageNums" slot="tip" class="el-upload__tip">已选取{{ imageList.length }}张图片</div>
          </el-upload>
        </el-row>
      </el-col>
      <el-col :span="11" style="margin-left: 20px">
        <el-row>
          {{ name }}后图片
        </el-row>
        <el-row>
          <el-card class="box-card display-image">
            <el-image :src="targetUrl" />
          </el-card>
        </el-row>
        <el-row>
          <el-button type="success" plain>下载当前{{ name }}图片</el-button>
          <el-button type="success" plain>下载所有{{ name }}图片</el-button>
        </el-row>
      </el-col>
    </div>
    <div class="rightArea">
      <el-row class="imageArea">
        <a
          v-for="(taskHistoryDetail, index) in taskHistoryDetailList"
          :key="index"
          href="#"
          :class="{active:index===isActive}"
          @click="selectImage(taskHistoryDetail, index)"
        >
          <div class="imgDiv">
            <el-image :src="taskHistoryDetail.originUrl" class="imgClass" :alt="taskHistoryDetail.originUrl">
              <div slot="placeholder" class="image-slot">
                加载中<span class="dot">...</span>
              </div>
            </el-image>
          </div>
        </a>
      </el-row>
      <el-row class="pageArea">
        <el-pagination
          v-if="taskHistoryDetailList.length > 0"
          class="pageContent"
          :current-page="page.currentPage"
          :page-sizes="[5]"
          :page-size="page.pageSize"
          :total="page.total"
          layout="prev, pager, next, total"
          @current-change="handlePageCurrentChange"
        />
      </el-row>
    </div>
  </el-card>
</template>

<script>
import { getDetailByTaskHistoryId, uploadImagesAndRestore } from '@/api/uploadAndRestore'
import { mapGetters } from 'vuex'

export default {
  name: 'ImageEnhance',
  props: {
    name: {
      type: String,
      default: ''
    },
    taskType: {
      type: Number,
      default: 0
    }
  },
  computed: {
    ...mapGetters([
      'username'
    ])
  },
  data() {
    return {
      originUrl: '',
      targetUrl: '',
      imageList: [],
      page: {
        // 总图片数目
        total: 0,
        // 当前页面是第几个  默认从1开始
        currentPage: 1,
        // 每一页显示的场景数目
        pageSize: 10
      },
      isActive: 0,
      showUploadImageNums: false,
      taskHistoryId: 0,
      taskHistoryDetailList: []
    }
  },
  methods: {
    handleChange(file, fileList) {
      this.imageList = fileList
      this.showUploadImageNums = true
    },
    async uploadImgAndRestore() {
      if (this.imageList.length === 0) {
        return
      }
      const imageFormData = new FormData()
      this.imageList.forEach(file => {
        imageFormData.append('images', file.raw, file.raw.name) // 此处一定是append file.raw 上传文件只需维护fileList file.raw.name要加上
      })
      imageFormData.append('username', this.username)
      imageFormData.append('taskType', this.taskType)
      uploadImagesAndRestore(imageFormData).then(res => {
        if (res.code === 200) {
          // 这里是导入完文件后，重新查询数据库刷新页面
          this.$message({
            type: 'success',
            message: '导入成功',
            duration: 1500
          })
          this.showUploadImageNums = false
          this.taskHistoryId = res.data.taskHistoryId
          this.page.total = res.data.total
          this.getDetailByPage()
          console.log('ttest')
        }
        this.imageList = []
      })
    },
    getDetailByPage() {
      const params = {
        start: (this.page.currentPage - 1) * this.page.pageSize + 1,
        pageSize: this.page.pageSize,
        taskHistoryId: this.taskHistoryId
      }
      console.log(params)
      getDetailByTaskHistoryId(params).then(res => {
        if (res.code === 200) {
          this.taskHistoryDetailList = res.data
        }
      })
    },
    // 修改当前所在页面的个数
    handlePageCurrentChange(currentPage) {
      this.page.currentPage = currentPage
      this.getDetailByPage()
    },
    selectImage(taskHistoryDetail, index) {
      this.originUrl = taskHistoryDetail.originUrl
      this.targetUrl = taskHistoryDetail.targetUrl
      this.isActive = index
    }
  }
}
</script>

<style scoped lang="scss">
.imageEnhance {
  position: absolute;
  left: 40px;
  height: 620px;
  width: 1250px;
  top: 30px;
}

.leftArea {
  position: absolute;
  left: 30px;
  height: 575px;
  width: 1030px;
}

.rightArea {
  position: absolute;
  height: 600px;
  width: 240px;
  right: 10px;
  min-width: 100px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin-bottom: 70px;

  a.active:before {
    content: "";
    position: absolute;
    background: rgba(87,50,236,0);
    height: 160px;
    left: 3px;
    right: 3px;
    border: 2px solid #6059f7;
  }
}

.imgDiv {
  overflow-x: hidden;
  overflow-y: hidden;
}

.imgClass {
  max-width: 205px;
  height: 150px;
  margin-top: 5px;
}

.imageArea {
  overflow: auto;
  margin-bottom: 10px;
}

.pageArea {
  display: flex;
  flex-direction: row;
  justify-content: flex-end;
  align-items: center;
}

.display-image {
  height: 470px;
  margin-top: 10px;
  margin-bottom: 20px;

  ::v-deep .el-image__inner {
    max-height: 430px;
  }
}
</style>
