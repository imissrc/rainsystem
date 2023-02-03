<template>
  <el-dialog
    title="修改密码"
    :visible.sync="changeVisible"
    width="50%"
  >
    <el-form ref="changeForm" :model="changeForm" label-width="70px" :rules="changeRules">
      <el-form-item prop="password">
        <el-input
          v-model="changeForm.oldPassword"
          placeholder="请输入老密码"
          name="oldPassword"
          tabindex="2"
          auto-complete="on"
          show-password
          prefix-icon="el-icon-key"
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="changeForm.newPassword1"
          placeholder="请输入新密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          show-password
          prefix-icon="el-icon-key"
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          v-model="changeForm.newPassword2"
          placeholder="请再次输入新密码"
          name="password"
          tabindex="2"
          auto-complete="on"
          show-password
          prefix-icon="el-icon-key"
        />
      </el-form-item>
    </el-form>
    <div slot="footer" class="dialog-footer">
      <el-button @click="changeVisible = false">取消</el-button>
      <el-button type="primary" @click="handlePassword">确认修改</el-button>
    </div>
  </el-dialog>
</template>

<script>
import { changePassword } from '@/api/login'
import { validPassword } from '@/utils/validate'

export default {
  name: 'ChangePassword',
  props: {
    changeVisible: {
      type: Boolean,
      default: false
    }
  },
  data() {
    const validatePassword = (rule, value, callback) => {
      if (!validPassword(value)) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      changeForm: {
        oldPassword: '',
        newPassword1: '',
        newPassword2: ''
      },
      // blur失去焦点
      changeRules: {
        password: [{ required: true, trigger: 'blur', validator: validatePassword }]
      },
      loading: false
    }
  },
  created() {

  },
  methods: {
    handlePassword() {
      this.$refs.changeForm.validate(valid => {
        if (valid) {
          this.loading = true
          changePassword(this.changeForm).then(res => {
            if (res.data.code === 0) {
              this.loading = false
              this.$message({
                type: 'success',
                message: res.data.message,
                duration: 3000,
                onClose: async() => {
                }
              })
            } else {
              const mes = res.data.message
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
