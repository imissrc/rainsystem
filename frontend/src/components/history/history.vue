<template>
  <div style="margin-top: -60px; margin-left: -8px; margin-right: -8px">
    <el-menu
      :default-active="navIndex"
      class="el-menu-demo"
      mode="horizontal"
      @select="handleSelect"
      background-color="#545c64"
      text-color="#fff"
      active-text-color="#ffd04b"
    >
      <el-menu-item index="home"><i class="el-icon-s-home"></i><span>主页</span></el-menu-item>
      <el-menu-item index="history"><i class="el-icon-time"></i><span>历史数据</span></el-menu-item>
      <el-submenu index="user" style="float: right">
        <template slot="title"><i class="el-icon-user"></i>用户管理</template>
        <el-menu-item index="logout">登出</el-menu-item>
        <el-menu-item index="changePassword">修改密码</el-menu-item>
      </el-submenu>
    </el-menu>

    <el-col :span="4">
      <el-menu
        :default-active="listQuery.historyIndex"
        class="el-menu-vertical-demo"
        @select="handleSelectHistory"
        >
        <el-menu-item :index="item" v-for="(item, index) in historyList" :key="item">
          <span slot="title">{{item}}</span>
          <span style="float: right"><el-button size="small" type="danger" icon="el-icon-delete" circle @click="delHistory(index, item)"></el-button></span>
        </el-menu-item>
      </el-menu>
    </el-col>
    <el-col :span="20">

    </el-col>
    <el-dialog
      title="修改密码"
      :visible.sync="changeVisible"
      width="30%">
      <el-form ref="changeForm" :model="changeForm" label-width="70px" :rules="changeRules">
        <el-form-item prop="oldPassword" label="老密码">
          <el-input
            v-model="changeForm.oldPassword"
            placeholder="请输入老密码"
            auto-complete="on"
            show-password
            prefix-icon="el-icon-key"
          />
        </el-form-item>
        <el-form-item prop="newPassword1" label="新密码">
          <el-input
            v-model="changeForm.newPassword1"
            placeholder="请输入新密码"
            auto-complete="on"
            show-password
            prefix-icon="el-icon-key"
          />
        </el-form-item>
        <el-form-item prop="newPassword2" label="新密码">
          <el-input
            v-model="changeForm.newPassword2"
            placeholder="请再次输入新密码"
            auto-complete="on"
            show-password
            prefix-icon="el-icon-key"
          />
        </el-form-item>
      </el-form>
      <div slot="footer" class="dialog-footer">
        <el-button @click="changeVisible = false">取消</el-button>
        <el-button type="primary" @click="handleChangePassword">确认修改</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import {getHistory, getHistoryTable, delHistory} from '@/api/history'
import {logout, changePassword} from '@/api/login'
// import Pagination from '@/components/pagination/Pagination'
import { validPassword } from '@/utils/validate'

let Base64 = require('js-base64').Base64

export default {
  // eslint-disable-next-line vue/multi-word-component-names
  name: 'history',
  // components: {Pagination},
  data () {
    const validatePassword = (rule, value, callback) => {
      if (!validPassword(value)) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      navIndex: 'history',
      listQuery: {
        historyIndex: '',
        page: 1,
        limit: 10
      },
      historyList: null,
      historyTable: null,
      total: 0,
      loading: false,
      fakeOptions: ['真', '假'],
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
    this.fetchHistory()
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
      } else if (key === 'history') {
        this.$router.push(`/history/`)
      } else if (key === 'logout') {
        this.logout()
      } else if (key === 'changePassword') {
        this.changeVisible = true
      }
    },
    fetchHistory () {
      getHistory().then(res => {
        if (res.data.code === 0) {
          this.historyList = res.data.historyList
          if (this.historyList) {
            this.listQuery.historyIndex = this.historyList[0]
          }
        }
      })
    },
    handleSelectHistory (key) {
      this.listQuery.historyIndex = key
      console.log(this.listQuery)
      this.loading = true
      getHistoryTable(this.listQuery).then(res => {
        if (res.data.code === 0) {
          this.total = res.data.total
          this.historyTable = res.data.file
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
    delHistory (index, item) {
      this.historyList.splice(index, 1)
      delHistory({'delValue': item}).then(res => {
        if (res.data.code === 0) {
          this.fetchHistory()
        }
      })
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
