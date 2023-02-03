<template>
  <div>
    <div class="historyList">
      <el-menu
        :default-active="listQuery.historyIndex"
        class="el-menu-vertical-demo"
        @select="handleSelectHistory"
      >
        <el-menu-item v-for="(item, index) in historyList" :key="item" :index="item">
          <span slot="title">{{ item }}</span>
          <span style="float: right"><el-button size="small" type="danger" icon="el-icon-delete" circle @click="delHistory(index, item)" /></span>
        </el-menu-item>
      </el-menu>
    </div>
    <el-card class="box-card imageEnhance">
      <div slot="header" class="clearfix" style="position: relative; left: -8%">
        <span>图像{{ name }}</span>
      </div>
      <div class="leftArea">
        <el-col :span="11">
          <el-row>
            原图片
          </el-row>
          <el-row>
            <el-card class="box-card display-image">
              <el-image :src="originImageUrl" />
            </el-card>
          </el-row>
        </el-col>
        <el-col :span="11" :offset="1">
          <el-row>
            {{ name }}后图片
          </el-row>
          <el-row>
            <el-card class="box-card display-image">
              <el-image :src="enhanceImageUrl" />
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
            v-for="(imgUrl, index) in imageUrlList"
            :key="index"
            href="#"
            :class="{active:index===isActive}"
            @click="selectImage(imgUrl, index)"
          >
            <div class="imgDiv">
              <el-image :src="imgUrl" class="imgClass" :alt="imgUrl">
                <div slot="placeholder" class="image-slot">
                  加载中<span class="dot">...</span>
                </div>
              </el-image>
            </div>
          </a>
        </el-row>
        <el-row class="pageArea">
          <el-pagination
            v-if="imageUrlList.length > 0"
            class="pageContent"
            :current-page="page.currentPage"
            :page-sizes="[5]"
            :page-size="page.pageSize"
            :total="page.total"
            layout="prev, pager, next, total"
            @size-change="handlePageSizeChange"
            @current-change="handlePageCurrentChange"
          />
        </el-row>
      </div>
    </el-card>
  </div>
</template>

<script>

export default {
  name: 'HistoryImageEnhance',
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
  data() {
    return {
      originImageUrl: 'http://10.109.246.53:8095/backend/resources/imageRaining/input-9ec134ba-a9f4-11ed-a9f2-2cea7feddecc.png',
      enhanceImageUrl: '',
      imageUrlList: ['http://10.109.246.53:8095/backend/resources/imageRaining/input-9ec134ba-a9f4-11ed-a9f2-2cea7feddecc.png',
        'http://10.109.246.53:8095/backend/resources/imageRaining/input-9ec134bb-a9f4-11ed-a9f2-2cea7feddecc.png'],
      imageList: [],
      page: {
        // 总图片数目
        total: 0,
        // 当前页面是第几个  默认从1开始
        currentPage: 1,
        // 每一页显示的场景数目
        pageSize: 5
      },
      isActive: 0,
      listQuery: {
        historyIndex: '',
        page: 1,
        limit: 10
      },
      historyList: []
    }
  },
  methods: {
    handleChange(file, fileList) {
      console.log(fileList)
      this.imageList = fileList
      this.showUploadImageNums = true
    },
    // 修改当前页面的显示列表数目
    handlePageSizeChange(pageSize) {
      this.page.pageSize = pageSize
      this.handlePageCurrentChange(this.page.currentPage)
    },
    // 修改当前所在页面的个数
    handlePageCurrentChange(currentPage) {
      this.page.currentPage = currentPage
      this.getAllImageInfos()
    },
    getAllImageInfos() {
      console.log('todo')
    },
    handleImageListChange() {
      console.log('todo')
    },
    selectImage(imgUrl, index) {
      this.originImageUrl = imgUrl
      this.isActive = index
      console.log('todo')
    }
  }
}
</script>

<style scoped lang="scss">
.historyList {
  position: absolute;
  left: 30px;
  height: 800px;
  width: 300px;
  top: 50px;
  background-color: #3A71A8;
}
.imageEnhance {
  position: absolute;
  right: 50px;
  height: 800px;
  width: 1300px;
  top: 50px;
}

.leftArea {
  position: absolute;
  left: 30px;
  height: 725px;
  width: 1000px;
}

.rightArea {
  position: absolute;
  height: 725px;
  width: 260px;
  right: 20px;
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
  max-width: 225px;
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
  height: 590px;
  margin-top: 10px;
  margin-bottom: 20px;

  ::v-deep .el-image__inner {
    max-height: 550px;
  }
}

.enhanceOpe {
  height: 600px;
  .el-button {
    margin-top: 300px;
  }
}
</style>
