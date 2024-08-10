<template>
  <div
    style="width: 500px; height: 450px; margin-top: 70px"
    class="bg-secondary rounded p-4 mx-auto"
  >
    <div class="row justify-content-center">
      <div class="col-md-10">
        <h2 class="text-center" v-show="!flagToChangeAdmin">Login</h2>
        <h2 class="text-center" v-show="flagToChangeAdmin">Sign Up</h2>
        <div class="mt-5 d-flex flex-column row-gap-4">
          <div class="form-group">
            <label class="mb-1" for="loginUsername">Username</label>
            <input
              type="text"
              class="form-control"
              id="loginUsername"
              placeholder="Enter username"
              v-model="uname"
            />
          </div>
          <div class="form-group">
            <label class="mb-1" for="loginPassword">Password</label>
            <input
              type="password"
              class="form-control"
              id="loginPassword"
              placeholder="Enter password"
              v-model="password"
            />
            <div class="mt-3" v-show="flagToChangeAdmin">
              <label for="adminOrUser">Are you an admin?</label>
              <input
                class="mx-2"
                type="checkbox"
                id="adminOrUser"
                v-model="isAdmin"
              />
            </div>
          </div>
          <button
            class="btn btn-dark btn-block w-50 mx-auto"
            @click="loginForm()"
            :disabled="!isFormValid"
          >
            {{ !flagToChangeAdmin ? "Login" : "Sign Up" }}
          </button>
        </div>
        <div class="mt-4" v-show="!flagToChangeAdmin" @click="toggleSignUp()">
          <div
            class="text-dark text-decoration-underline"
            style="float: right; cursor: pointer"
          >
            Didn't sign up yet? Sign up here
          </div>
        </div>
        <div class="mt-4" v-show="flagToChangeAdmin" @click="toggleSignUp()">
          <div
            class="text-dark text-decoration-underline"
            style="float: right; cursor: pointer"
          >
            Already signed up? Login here
          </div>
        </div>
      </div>
    </div>
  </div>
  <div
    v-if="showAlert"
    :class="[
      'alert',
      alertClass,
      'alert-dismissible',
      'fade',
      'show',
      'mx-auto',
    ]"
    role="alert"
    style="width: 500px; margin-top: 10px"
  >
    {{ alertMessage }}
    <button
      type="button"
      class="btn-close"
      @click="showAlert = false"
      aria-label="Close"
    ></button>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      uname: "",
      password: "",
      isAdmin: true,
      flagToChangeAdmin: false,
      showAlert: false,
      alertMessage: "",
      alertClass: "",
    };
  },
  computed: {
    isFormValid() {
      return this.uname.trim() !== "" && this.password.trim() !== "";
    },
  },
  methods: {
    loginForm() {
      if (this.flagToChangeAdmin == false) {
        axios
          .post("http://127.0.0.1:5000/loginUser", {
            userName: this.uname,
            password: this.password,
          })
          .then((response) => {
            console.log(response);
            if (response.status == 200) {
              localStorage.setItem("role", response.data.Role);
              localStorage.setItem("username", response.data.Name);
              this.alertMessage = "Login successful!";
              this.alertClass = "alert-success";
              this.showAlert = true;
              if (response.data.Role == 1) {
                this.$router.push("/admin-home");
              } else {
                this.$router.push("/user-home");
              }
            } else {
              this.alertMessage = response.data.ERROR;
              this.alertClass = "alert-danger";
              this.showAlert = true;
            }
          })
          .catch((error) => {
            this.alertMessage = "Login failed. Please try again.";
            this.alertClass = "alert-danger";
            this.showAlert = true;
          });
      } else {
        axios
          .post("http://127.0.0.1:5000/addUser", {
            userName: this.uname,
            password: this.password,
            isAdmin: this.isAdmin,
          })
          .then((response) => {
            console.log(response);
            if (response.status == 200) {
              this.flagToChangeAdmin = false;
              this.uname = "";
              this.password = "";
              this.alertMessage = "Sign up successful!";
              this.alertClass = "alert-success";
              this.showAlert = true;
            }
          })
          .catch((error) => {
            this.alertMessage = "Sign up failed. Please try again.";
            this.alertClass = "alert-danger";
            this.showAlert = true;
          });
      }
    },
    toggleSignUp() {
      this.flagToChangeAdmin = !this.flagToChangeAdmin;
    },
  },
  mounted() {
    localStorage.removeItem("role");
    localStorage.removeItem("username");
    axios.get("http://127.0.0.1:5000/logOut")
  },
};
</script>
