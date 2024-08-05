export default {
  install(app) {
    app.config.globalProperties.$checkUserRole = function (roleString) {
      const role = localStorage.getItem("role");
      console.log(role)
      if (roleString == "admin" && role != 1) {
        this.$router.push("/error-page");
      } else if (roleString == "user" && role != 0) {
        this.$router.push("/error-page");
      }
    };
  },
};
