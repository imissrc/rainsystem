const getters = {
  sidebar: state => state.app.sidebar,
  size: state => state.app.size,
  device: state => state.app.device,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  loginState: state => state.user.loginState,
  username: state => state.user.username,
  errorLogs: state => state.errorLog.logs
}
export default getters
