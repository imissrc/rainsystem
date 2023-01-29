<template>
  <div>
    <el-card shadow="never">
      <el-row>
        <el-col :span="2" :offset="22">
          <el-tooltip class="item" effect="dark" content="删除数据" placement="top">
            <el-button size="mini" type="danger" circle icon="el-icon-delete" @click="deleteMe"/>
          </el-tooltip>
        </el-col>
      </el-row>
      <el-form ref="itemform" :model="item" label-width="70px">
        <el-form-item label="文本">
          <el-col :span="20">
            <el-input
              type="textarea"
              placeholder="text"
              v-model="item.text"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="图片">
          <el-col :span="20">
            <el-upload
              class="upload-demo"
              ref="uploadImage"
              drag
              action="resources/data/image/"
              multiple
              accept="image/jpeg,image/gif,image/png"
              list-type="picture"
              :auto-upload="false"
              :on-change="handleImageListChange"
            >
              <i class="el-icon-upload"></i>
              <div class="el-upload__text">将图片拖到此处，或<em>点击上传</em></div>
              <div class="el-upload__tip" slot="tip">只能上传图片</div>
            </el-upload>
          </el-col>
        </el-form-item>
        <el-form-item label="性别">
          <el-col :span="20">
            <el-input
              placeholder="userGender"
              v-model="item.userGender"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="关注数">
          <el-col :span="20">
            <el-input
              placeholder="userFollowCount"
              v-model="item.userFollowCount"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="粉丝数">
          <el-col :span="20">
            <el-input
              placeholder="userFansCount"
              v-model="item.userFansCount"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="微博数">
          <el-col :span="20">
            <el-input
              placeholder="userWeiboCount"
              v-model="item.userWeiboCount"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="用户位置">
          <el-col :span="20">
            <el-input
              placeholder="userLocation"
              v-model="item.userLocation"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="用户描述">
          <el-col :span="20">
            <el-input
              placeholder="userDescription"
              v-model="item.userDescription"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
        <el-form-item label="类别">
          <el-col :span="20">
            <el-input
              placeholder="category"
              v-model="item.category"
              clearable>
            </el-input>
          </el-col>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script>
export default {
  name: 'ManualView',
  props: {
    index: {
      type: Number,
      default: 0
    },
    item: {
      type: Object,
      default: null
    }
  },
  data () {
    return {
      imageList: null
    }
  },
  methods: {
    deleteMe: function () {
      this.$emit('deleteIndex', this.index)
    },
    handleImageListChange (file, fileList) {
      this.item.imageList = fileList
      // this.$emit('handleImageListChange')
      return true
    }
  }
}
</script>

<style scoped>

</style>
