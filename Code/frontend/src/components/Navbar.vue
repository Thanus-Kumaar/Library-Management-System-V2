<!-- Navbar -->
<template>
  <nav
    class="navbar navbar-expand-lg mx-auto px-4 mt-3"
    style="
      background-color: rgba(40, 40, 50, 0.7);
      width: 60%;
      border-radius: 8px;
    "
  >
    <div class="container-fluid">
      <div class="navbar-brand" style="color: white">{{ navbarTitle }}</div>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <a
            v-if="isAdmin == 1"
            class="nav-link"
            :class="{ active: isActive('/admin-home') }"
            @click="navigate('/admin-home')"
            style="color: white; cursor: pointer;"
            >Home</a
          >
          <a
            v-if="isAdmin == 1"
            class="nav-link"
            :class="{ active: isActive('/manage-sections') }"
            @click="navigate('/manage-sections')"
            style="color: white; cursor: pointer;"
            >Sections</a
          >
          <a
            v-if="isAdmin == 1"
            class="nav-link"
            :class="{ active: isActive('/manage-books') }"
            @click="navigate('/manage-books')"
            style="color: white; cursor: pointer;"
            >Books</a
          >
          <a
            v-if="isAdmin == 1"
            class="nav-link"
            :class="{ active: isActive('/manage-issue-revoke') }"
            @click="navigate('/manage-issue-revoke')"
            style="color: white; cursor: pointer;"
            >Issue/Revoke</a
          >
          <a
            v-if="isAdmin == 1"
            class="nav-link"
            :class="{ active: isActive('/search-books') }"
            @click="navigate('/search-books')"
            style="color: white; cursor: pointer;"
            >Search</a
          >
          <a
            v-if="isAdmin == 0"
            class="nav-link"
            :class="{ active: isActive('/user-home') }"
            @click="navigate('/user-home')"
            style="color: white; cursor: pointer; margin-left: 180px;"
            >Home</a
          >
          <a
            v-if="isAdmin == 0"
            class="nav-link"
            :class="{ active: isActive('/read-books') }"
            @click="navigate('/read-books')"
            style="color: white; cursor: pointer;"
            >Read</a
          >
          <a
            v-if="isAdmin == 0"
            class="nav-link"
            :class="{ active: isActive('/user-books') }"
            @click="navigate('/user-books')"
            style="color: white; cursor: pointer;"
            >Request</a
          >
          <a href="/login" v-if="isAdmin == 2">
            <button type="button" class="btn btn-secondary" style="margin-left: 310px;">
              Sign Up / Login
            </button>
          </a>
          <button v-if="isAdmin!=2" type="button" class="btn btn-secondary" @click="logout" style="margin-left: 10px;">
            Log out
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from "axios";
export default {
  data() {
    return {
      isAdmin: this.getRoleFromLocalStorage(),
    };
  },
  computed: {
    navbarTitle() {
      return this.isAdmin
        ? "Library Management System"
        : "Library Management System";
    },
  },
  methods: {
    isActive(route) {
      return this.$route.path === route;
    },
    navigate(route) {
      this.$router.push(route);
    },
    logout() {
      localStorage.removeItem("role");
      localStorage.removeItem("username");
      axios.get("http://127.0.0.1:5000/logOut").then((response) => {
        console.log(response);
        if (response.status == 200) {
          this.$router.replace("/");
        }
      });
    },
    getRoleFromLocalStorage() {
      const role = localStorage.getItem("role");
      if (role === "1"){
        return 1
      } else if (role === "0"){
        return 0
      }
      return 2;
    },
  },
  watch: {
    $route(to, from) {
      this.isAdmin = this.getRoleFromLocalStorage();
    },
  },
};
</script>
