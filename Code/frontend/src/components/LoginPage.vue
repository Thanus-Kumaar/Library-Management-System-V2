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
              <input class="mx-2" type="checkbox" id="adminOrUser" v-model="isAdmin" />
            </div>
          </div>
          <button
            class="btn btn-dark btn-block w-50 mx-auto"
            @click="loginForm()"
          >
            {{ !flagToChangeAdmin ? "Login" : "SignUp" }}
          </button>
        </div>
        <div class="mt-4" v-show="!flagToChangeAdmin"  @click="toggleSignUp()">
          <div class="text-dark text-decoration-underline" style="float: right; cursor: pointer;"
            >Didn't sign up yet? Sign in here</div
          >
        </div>
        <div class="mt-4" v-show="flagToChangeAdmin"  @click="toggleSignUp()">
          <div class="text-dark text-decoration-underline" style="float: right; cursor: pointer;"
            >Already signed in? Login here</div
          >
        </div>
      </div>
    </div>
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
      flagToChangeAdmin: false
    };
  },
  methods: {
    loginForm() {
      if (this.flagToChangeAdmin == false){
        axios
        .post("http://127.0.0.1:5000/loginUser", {
          userName: this.uname,
          password: this.password,
        })
        .then((response) => {
          console.log(response);
          if (response.status == 200){
            localStorage.setItem('role', response.data.Role)
            if (response.data.Role == 1){
              this.$router.push('/admin-home')
            }
          }
        });
      } else {
        axios
        .post("http://127.0.0.1:5000/addUser", {
          userName: this.uname,
          password: this.password,
          isAdmin: this.isAdmin
        })
        .then((response) => {
          console.log(response);
          if (response.status == 200){
            this.flagToChangeAdmin = false
            this.uname == ""
            this.password == ""
          }
        });
      }
      
    },
    toggleSignUp() {
      this.flagToChangeAdmin = !this.flagToChangeAdmin
    }
  },
};
</script>
