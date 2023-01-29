<template>
  <div>
    <div style="margin-top: -60px; margin-left: -8px; margin-right: -8px">
      <el-menu
        :default-active="activeIndex"
        class="el-menu-demo"
        mode="horizontal"
        @select="handleSelect"
        background-color="#545c64"
        text-color="#fff"
        active-text-color="#ffd04b"
      >
        <el-menu-item index="home"><i class="el-icon-s-home"></i><span>主页</span></el-menu-item>
        <el-menu-item index="history"><i class="el-icon-time"></i><span>历史数据</span></el-menu-item>
        <el-menu-item index="manual"><i class="el-icon-document-add"></i>输入数据</el-menu-item>
        <el-menu-item index="importFile"><i class="el-icon-upload"></i>导入数据</el-menu-item>
        <el-menu-item index="runPredict"><i class="el-icon-video-play"></i>运行</el-menu-item>
        <el-menu-item index="stopPredict"><i class="el-icon-video-pause"></i>停止运行</el-menu-item>
        <el-menu-item index="saveHistory"><i class="el-icon-finished"></i>存储历史</el-menu-item>
        <el-menu-item index="exportTable" :loading="exportLoading"><i class="el-icon-download"></i>导出</el-menu-item>
<!--        <el-menu-item index="startReadyImages">准备图片数据</el-menu-item>-->
        <el-menu-item>
          <el-tag
            size="medium"
            :type="taskStatus | statusFilter"
          >{{ statusOptions[taskStatus] }}
          </el-tag>
        </el-menu-item>
<!--        <el-menu-item>-->
<!--          <el-tag-->
<!--            size="medium"-->
<!--          >准确率：{{ accuracy }}-->
<!--          </el-tag>-->
<!--        </el-menu-item>-->
        <el-submenu index="user" style="float: right">
          <template slot="title"><i class="el-icon-user"></i>用户管理</template>
          <el-menu-item index="logout">登出</el-menu-item>
          <el-menu-item index="changePassword">修改密码</el-menu-item>
        </el-submenu>
      </el-menu>
    </div>

      <el-row style="margin-top: 15px">
        <el-col :span="3">
          <el-button size="small" type="success" @click="addManualForm">添加数据</el-button>
        </el-col>
      </el-row>
      <span slot="footer" class="dialog-footer">
        <el-button @click="manualVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </span>
  </div>
</template>
<!--在一个普通函数中，this归属于函数的“拥有者”。由于我们是在vue组件里定义的，那么this归属于vue组件。-->
<!--在一个箭头函数里，this并不归属于函数的拥有者。-->
<script>
import {uploadFile, runPredictFile, uploadImage, home, stopPredictFile, readyImages, uploadManual, downloadData} from '@/api/home'
import {saveHistory} from '@/api/history'
// import Pagination from '@/components/pagination/Pagination'
import XLSX from 'xlsx'
// import ManualView from '@/components/home/Manual'
import { parseTime } from '@/utils'
import {logout, changePassword} from '@/api/login'

import { validPassword } from '@/utils/validate'

var itemData = {
  id: '',
  text: '',
  piclist: '',
  userGender: '',
  userFollowCount: '',
  userFansCount: '',
  userWeiboCount: '',
  userLocation: '',
  userDescription: '',
  category: '',
  imageList: null
}
let Base64 = require('js-base64').Base64

export default {
  name: 'home',
  // components: {ManualView, Pagination},
  filters: {
    statusFilter (status) {
      const statusMap = {
        0: 'success',
        1: 'danger'
      }
      return statusMap[status]
    }
  },
  data () {
    const validatePassword = (rule, value, callback) => {
      if (!validPassword(value)) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      filename: '',
      importTitle: '',
      importVisible: false,
      file: null,

      imageList: null,

      manualVisible: false,
      manualTitle: '',
      csvData: {
        header: null,
        results: null
      },
      tableData: [
        {
          id: null,
          text: '',
          piclist: null,
          userGender: '',
          userFollowCount: 0,
          userFansCount: 0,
          userWeiboCount: 0,
          userLocation: '',
          userDescription: '',
          category: '',
          label: 0
        }
      ],
      formData: [],
      uploading: false,
      statusOptions: ['空闲', '运行中'],
      taskStatus: 0,
      activeIndex: 'home',
      accuracy: 0,
      loading: false,
      total: 0,
      listQuery: {
        page: 1,
        limit: 10
      },
      fakeOptions: ['真', '假'],
      exportLoading: false,
      exportDataList: null,
      autoWidth: true,
      bookType: 'xlsx',
      changeVisible: false,
      changeForm: {
        oldPassword: '',
        newPassword1: '',
        newPassword2: ''
      },
      // blur失去焦点
      changeRules: {
        oldPassword: [{required: true, trigger: 'blur', validator: validatePassword}],
        newPassword1: [{required: true, trigger: 'blur', validator: validatePassword}],
        newPassword2: [{required: true, trigger: 'blur', validator: validatePassword}]
      },
      changeloading: false
    }
  },
  created () {
    this.fetchTable()
  },
  methods: {
    getImageName (image) {
      image = Base64.decode(image)
      return image
    },
    getImage (image) {
      return 'data:image/jpg;base64,' + image
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
    fetchTable () {
      this.loading = true
      home(this.listQuery).then(res => {
        if (res.data.code === 0) {
          this.total = res.data.total
          this.tableData = res.data.file
          this.taskStatus = res.data.taskStatus
          this.accuracy = res.data.accuracy
          this.loading = false
        } else if (res.data.code === 400) {
          this.$message({
            type: 'success',
            message: res.data.message,
            duration: 1500,
            onClose: async () => {
            }
          })
          this.loading = false
        }
      })
    },
    // beforeImageUpload(file) {
    //   const isIMAGE = file.type === 'image/jpeg' || 'image/gif' || 'image/png';
    //   if (!isIMAGE) {
    //     this.$message.error('上传文件只能是图片格式!');
    //     return
    //   }
    //   return false
    // },
    openManualDialog () {
      this.manualVisible = true
      this.manualTitle = '输入数据'
      this.formData = []
    },
    openImportDialog () {
      this.file = null
      this.filename = ''
      this.imageList = null
      this.importVisible = true
      this.importTitle = '导入文件'
      if (this.$refs.uploadCsv) {
        this.$refs.uploadCsv.clearFiles()
      }
      if (this.$refs.uploadImage) {
        this.$refs.uploadImage.clearFiles()
      }
    },
    // on-change: 文件状态改变时的钩子，添加文件、上传成功和上传失败时都会被调用
    handleCsvChange (file) {
      // const isLt = file.size / 1024 / 1024 < 0.1
      const isLt = file.size / 1024 / 1024 < 20
      const isCsv = file.raw.type === 'text/csv'
      if (!isLt) {
        this.$message.warning('上传文件大小不能超过 ' + 0.1 * 1000 + 'K')
        this.uploading = false
        this.$refs.uploadCsv.clearFiles()
        return false
      }
      if (!isCsv) {
        this.$message.warning('只能上传csv格式文件')
        this.uploading = false
        this.$refs.uploadImage.clearFiles()
        return false
      }
      this.filename = file.name
      this.file = file.raw
      this.uploading = true
      return true
    },
    handleImageChange (file, fileList) {
      this.imageList = fileList
      const isIMAGE = file.raw.type === 'image/jpeg' || 'image/gif' || 'image/png'
      if (!isIMAGE) {
        this.$message.error('上传文件只能是图片格式!')
        return false
      }
      return true
    },
    async importFiles () {
      // this.importCsv()
      // this.importImage()
      this.importVisible = false
    },
    async importCsv () {
      let fileFormData = new FormData()
      fileFormData.set('file', this.file, this.filename)
      // 箭头函数里面的this没有指向当前vue实例
      // {headers: { "Content-type": "multipart/form-data" }}
      if (this.filename !== '' && this.uploading) {
        // this.$refs.uploadCsv.submit();
        uploadFile(fileFormData).then(res => {
          if (res.data.code === 0) {
            // this.csvVisible = false;
            // this.readCsv(fileFormData.get('file'));
            // 这里是导入完文件后，重新查询数据库刷新页面
            this.$message({
              type: 'success',
              message: '导入成功',
              duration: 1500,
              onClose: async () => {
                // this.csvVisible = false
              }
            })
            this.fetchTable()
          }
        })
      } else {
        this.$message.error('上传文件不能为空')
      }
    },
    async importImage () {
      let imageFormData = new FormData()
      this.imageList.forEach(file => {
        imageFormData.append('images', file.raw, file.raw.name) // 此处一定是append file.raw 上传文件只需维护fileList file.raw.name要加上
      })
      // {headers: { "Content-type": "multipart/form-data" }}
      if (this.imageList !== null) {
        uploadImage(imageFormData).then(res => {
          if (res.data.code === 0) {
            // 这里是导入完文件后，重新查询数据库刷新页面
            this.$message({
              type: 'success',
              message: '导入成功',
              duration: 1500,
              onClose: async () => {
              }
            })
            this.fetchTable()
          }
        })
      } else {
        this.$message.error('上传图片不能为空')
      }
    },
    runPredict () {
      runPredictFile().then(res => {
        this.taskStatus = res.data.taskStatus
        if (res.data.code === 0) {
          this.$message({
            type: 'success',
            message: '启动成功',
            duration: 1500
          })
        } else {
          this.$message({
            type: 'error',
            message: '启动失败',
            duration: 1500
          })
        }
      })
    },
    stopPredict () {
      stopPredictFile().then(res => {
        this.taskStatus = res.data.taskStatus
        if (res.data.code === 0) {
          this.$message({
            type: 'success',
            message: '停止运行',
            duration: 1500
          })
        } else {
          this.$message({
            type: 'error',
            message: '停止失败',
            duration: 1500
          })
        }
      })
    },
    readCsv (rawFile) {
      return new Promise((resolve) => {
        const reader = new FileReader()
        reader.onload = e => {
          var data = e.target.result
          const workbook = XLSX.read(data, {type: 'array'})
          const firstSheetName = workbook.SheetNames[0]
          const worksheet = workbook.Sheets[firstSheetName]
          const header = this.getHeaderRow(worksheet)
          const results = XLSX.utils.sheet_to_json(worksheet)
          // const result_csv = XLSX.utils.sheet_to_csv(worksheet);
          this.generateData({header, results})
          resolve()
        }
        reader.readAsArrayBuffer(rawFile)
      })
    },
    getHeaderRow (sheet) {
      const headers = []
      const range = XLSX.utils.decode_range(sheet['!ref'])
      let C
      const R = range.s.r
      /* start in the first row */
      for (C = range.s.c; C <= range.e.c; ++C) { /* walk every column in the range */
        const cell = sheet[XLSX.utils.encode_cell({c: C, r: R})]
        /* find the cell in the first row */
        let hdr = 'UNKNOWN ' + C // <-- replace with your desired default
        if (cell && cell.t) hdr = XLSX.utils.format_cell(cell)
        headers.push(hdr)
      }
      return headers
    },
    generateData ({header, results}) {
      this.csvData.header = header
      this.csvData.results = results
    },
    startReadyImages () {
      readyImages().then(res => {
        if (res.data.code === 0) {
          this.$message({
            type: 'success',
            message: '图片数据准备成功',
            duration: 1500
          })
        }
      })
    },
    addManualForm () {
      this.formData.push(JSON.parse(JSON.stringify(itemData)))
    },
    deleteManualForm (index) {
      if (this.formData.length > 0) {
        this.formData.splice(index, 1)
      }
    },
    async submitForm () {
      if (this.formData.length > 0) {
        var count = 0
        var imageFormData = new FormData()
        for (var i = 0; i < this.formData.length; i++) {
          var data = this.formData[i].imageList
          if (data) {
            for (var j = 0; j < data.length; j++) {
              imageFormData.append('images', data[j].raw, data[j].raw.name)
              if (j < data.length - 1) {
                this.formData[i].piclist += data[j].raw.name + '\t'
              } else {
                this.formData[i].piclist += data[j].raw.name
              }
              count += 1
            }
          }
          delete this.formData[i].imageList
        }
        uploadManual(this.formData).then(res => {
          if (res.data.code === 0) {
            if (count > 0) {
              uploadImage(imageFormData).then(resTwo => {
                if (resTwo.data.code === 0) {
                  this.formData = []
                  this.manualVisible = false
                  this.$message({
                    type: 'success',
                    message: '上传成功',
                    duration: 1500,
                    onClose: async () => {
                    }
                  })
                }
              })
            }
          }
        })
      } else {
        this.$message.error('上传数据不能为空')
      }
    },
    // handleImageListChange () {
    // },
    storeHistory () {
      saveHistory().then(res => {
        if (res.data.code === 0) {
          this.$message({
            type: 'success',
            message: '保存成功',
            duration: 1500,
            onClose: async () => {
            }
          })
        }
      })
    },
    exportData () {
      this.exportLoading = true
      downloadData().then(res => {
        if (res.data.code === 0) {
          import('@/utils/Export2Excel').then(excel => {
            const tHeader = ['id', 'text', 'piclist', 'userGender', 'userFollowCount', 'userFansCount', 'userWeiboCount', 'userLocation', 'userDescription', 'category', 'label']
            const filterVal = ['id', 'text', 'piclist', 'userGender', 'userFollowCount', 'userFansCount', 'userWeiboCount', 'userLocation', 'userDescription', 'category', 'label']
            const list = res.data.file
            const data = this.formatJson(filterVal, list)
            excel.export_json_to_excel({
              header: tHeader,
              data,
              filename: res.data.filename,
              autoWidth: this.autoWidth,
              bookType: this.bookType
            })
            this.$message({
              type: 'success',
              message: '导出成功',
              duration: 1500,
              onClose: async () => {
              }
            })
            this.exportLoading = false
          })
        }
      })
    },
    formatJson (filterVal, jsonData) {
      return jsonData.map(v => filterVal.map(j => {
        if (j === 'timestamp') {
          return parseTime(v[j])
        } else {
          return v[j]
        }
      }))
    },
    logout () {
      logout().then(res => {
        if (res.data.code === 0) {
          this.$router.push({path: '/'})
          this.$message({
            type: 'success',
            message: '你已成功登出',
            duration: 1500,
            onClose: async () => {
            }
          })
        }
      })
    },
    handleChangePassword () {
      this.$refs.changeForm.validate(valid => {
        if (valid) {
          if (this.changeForm.newPassword1 === this.changeForm.newPassword2) {
            this.changeloading = true
            changePassword(this.changeForm).then(res => {
              if (res.data.code === 0) {
                this.changeloading = false
                this.changeForm.oldPassword = ''
                this.changeForm.newPassword1 = ''
                this.changeForm.newPassword2 = ''
                this.changeVisible = false
                this.$message({
                  type: 'success',
                  message: res.data.message,
                  duration: 3000,
                  onClose: async () => {
                  }
                })
              } else {
                var mes = res.data.message
                this.$message(mes)
                this.changeloading = false
              }
            }).catch(() => {
              this.changeloading = false
            })
          } else {
            this.$message({
              type: 'error',
              message: '密码不一致',
              duration: 1500,
              onClose: async () => {
              }
            })
          }
        }
      })
    }
  }
}
</script>

<style scoped>

</style>
