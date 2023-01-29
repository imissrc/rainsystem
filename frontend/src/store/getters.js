const getters = {
  sidebar: state => state.app.sidebar,
  size: state => state.app.size,
  device: state => state.app.device,
  visitedViews: state => state.tagsView.visitedViews,
  cachedViews: state => state.tagsView.cachedViews,
  // token: state => state.user.token,
  // infoId: state => state.user.infoId,
  loginName: state => state.user.username,
  // avatar: state => state.user.avatar,
  errorLogs: state => state.errorLog.logs,
}
export default getters
