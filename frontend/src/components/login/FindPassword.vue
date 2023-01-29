<template>
  <div class="register">
    <el-form ref="findForm" :model="findForm" :rules="registerRules" class="register-form" auto-complete="on"
             label-position="left">
      <div class="title-container">
        <h2 class="title">找回密码</h2>
      </div>

      <el-form-item prop="username">
        <el-input
          ref="username"
          v-model="findForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
          prefix-icon="el-icon-user-solid"
        />
      </el-form-item>
      <el-form-item prop="email">
        <el-input
          ref="email"
          v-model="findForm.email"
          placeholder="Email"
          name="email"
          tabindex="2"
          auto-complete="on"
          prefix-icon="el-icon-message"
        />
      </el-form-item>
      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:20px;"
                 @click.native.prevent="handlePassword">找回密码
      </el-button>
    </el-form>

  </div>
</template>

<script>
import {findPassword} from '@/api/login'
import { validUsername } from '@/utils/validate'

export default {
  name: 'FindPassword',
  data () {
    const validateUsername = (rule, value, callback) => {
      // trim 表示字符串去除字符串最左边和最右边的空格
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    return {
      findForm: {
        username: '',
        email: ''
      },
      // blur失去焦点
      registerRules: {
        username: [{required: true, trigger: 'blur', validator: validateUsername}],
        email: [
          { required: true, message: '请输入邮箱地址', trigger: 'blur' },
          { type: 'email', message: '请输入正确的邮箱地址', trigger: ['blur', 'change'] }
        ]
      },
      loading: false
    }
  },
  methods: {
    handlePassword () {
      this.$refs.findForm.validate(valid => {
        if (valid) {
          this.loading = true
          findPassword(this.findForm).then(res => {
            if (res.data.code === 0) {
              this.$router.push({path: '/'})
              this.loading = false
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
              this.loading = false
            }
          }).catch(() => {
            this.loading = false
          })
        }
      })
    }
  }
}
</script>

<style scoped>
  .register {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-image: url(../../assets/images/background.gif);
    background-size: 100%;
    background-repeat: no-repeat;
  }

  .register-form {
    width: 400px;
    height: 300px;
    padding: 13px;
    position: absolute;
    left: 50%;
    top: 50%;
    margin-left: -200px;
    margin-top: -200px;

    background-color: rgba(240, 255, 255, 0.5);

    border-radius: 10px;
    text-align: center;
  }
</style>
