<template>
  <div class="login">
    <div class="login-title">图像恢复系统</div>
    <el-form ref="loginForm" :model="loginForm" :rules="loginRules" class="login-form" auto-complete="on"
             label-position="left">
      <div class="title-container">
        <h2 class="title">登录</h2>
      </div>

      <el-form-item prop="username">
        <el-input
          ref="username"
          v-model="loginForm.username"
          placeholder="Username"
          name="username"
          type="text"
          tabindex="1"
          auto-complete="on"
          prefix-icon="el-icon-user"
        />
      </el-form-item>
      <el-form-item prop="password">
        <el-input
          ref="password"
          v-model="loginForm.password"
          placeholder="Password"
          name="password"
          tabindex="2"
          auto-complete="on"
          @keyup.enter.native="handleLogin"
          show-password
          prefix-icon="el-icon-key"
        />
      </el-form-item>

      <el-button :loading="loading" type="primary" style="width:100%;margin-bottom:20px;"
                 @click.native.prevent="handleLogin">Login
      </el-button>
      <div class="login_control">
        <router-link :to="'/register'" class="goRegister" style="font-size: small">
          <span>还没有账户? 立即注册</span>
        </router-link>
<!--        <router-link :to="'/changePassword'" class="changePassword"  style="font-size: 12px">-->
<!--          <span>修改密码</span>-->
<!--        </router-link>-->
        <router-link :to="'/findPassword'" class="findPassword"  style="font-size: 12px">
          <span>忘记密码</span>
        </router-link>
      </div>
    </el-form>
  </div>
</template>

<script>
import { login } from '@/api/login'
import { validUsername, validPassword } from '@/utils/validate'

export default {
   // eslint-disable-next-line vue/multi-word-component-names
  name: 'Login',
  data () {
    const validateUsername = (rule, value, callback) => {
      // trim 表示字符串去除字符串最左边和最右边的空格
      if (!validUsername(value)) {
        callback(new Error('Please enter the correct user name'))
      } else {
        callback()
      }
    }
    const validatePassword = (rule, value, callback) => {
      if (!validPassword(value)) {
        callback(new Error('The password can not be less than 6 digits'))
      } else {
        callback()
      }
    }
    return {
      loginForm: {
        username: 'imissrc',
        password: '123456'
      },
      // blur失去焦点
      loginRules: {
        username: [{required: true, trigger: 'blur', validator: validateUsername}],
        password: [{required: true, trigger: 'blur', validator: validatePassword}]
      },
      loading: false
    }
  },
  methods: {
    handleLogin () {
      this.$refs.loginForm.validate(valid => {
        if (valid) {
          this.loading = true
          login(this.loginForm).then(res => {
            if (res.data.code === 0) {
              this.$router.push({path: '/dashboard'})
              this.loading = false
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
  .login {
    position: absolute;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-image: url(../../assets/images/background.gif);
    background-size: 100%;
    background-repeat: no-repeat;
  }

  .login-title {
    width: 500px;
    font-size: 50px;
    position: absolute;
    top: 200px;
    left: 50%;
    margin-left: -200px;
  }

  .login-form {
    width: 400px;
    height: 280px;
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

  .goRegister {
    margin-left: -5px;
  }

  /*.changePassword {*/
  /*  margin-left: 160px;*/
  /*}*/
  .findPassword {
    margin-left: 215px;
  }
  .login_control {
    margin-left: -2px;
  }
</style>