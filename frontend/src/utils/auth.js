import Cookies from 'js-cookie'

const UserNameKey = 'username'// 登陆姓名

export function getUserName() {
  return Cookies.get(UserNameKey)
}

export function setUserName(name) {
  return Cookies.set(UserNameKey, name)
}

export function removeUserName() {
  return Cookies.remove(UserNameKey)
}