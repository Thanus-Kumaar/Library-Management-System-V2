<!-- Navbar -->
<template>
  <nav class="navbar navbar-expand-lg mx-auto px-4 mt-3" style="background-color: rgba(40, 40, 50, 0.7); width: 60%; border-radius: 8px;">
    <div class="container-fluid">
      <div class="navbar-brand" style="color: white;">{{ navbarTitle }}</div>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <a v-if="isAdmin" class="nav-link" :class="{ active: isActive('/adminHome') }" @click="navigate('/adminHome')" style="color: white;">Home</a>
          <a v-if="isAdmin" class="nav-link" :class="{ active: isActive('/manageSections') }" @click="navigate('/manageSections')" style="color: white;">Sections</a>
          <a v-if="isAdmin" class="nav-link" :class="{ active: isActive('/manageBooks') }" @click="navigate('/manageBooks')" style="color: white;">Books</a>
          <a v-if="!isAdmin" class="nav-link" :class="{ active: isActive('/userHome') }" @click="navigate('/userHome')" style="color: white;">Home</a>
          <a v-if="!isAdmin" class="nav-link" :class="{ active: isActive('/readBooks') }" @click="navigate('/readBooks')" style="color: white;">Read</a>
          <a v-if="!isAdmin" class="nav-link" :class="{ active: isActive('/userBooks') }" @click="navigate('/userBooks')" style="color: white;">Request</a>
          <button type="button" class="btn btn-secondary" @click="logout">Log out</button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
import axios from 'axios'
export default {
  data() {
    return {
      isAdmin: localStorage.getItem('role') == 1 ? 1 : localStorage.getItem('role') == 0 ? 0 : -1,
    };
  },
  computed: {
    navbarClass() {
      return this.isAdmin ? 'navbar navbar-expand-lg bg-body-tertiary' : 'navbar navbar-expand-lg bg-body-tertiary';
    },
    navbarTitle() {
      return this.isAdmin ? 'Library Management System' : 'Library Management System';
    }
  },
  methods: {
    isActive(route) {
      return this.$route.path === route;
    },
    navigate(route) {
      this.$router.push(route);
    },
    logout() {
      localStorage.removeItem('role');
      localStorage.removeItem('username');
      axios.get("http://127.0.0.1:5000/logOut")
      .then((response)=>{
        console.log(response)
        if(response.status==200){
          this.$router.replace('/');
        }
      })
    }
  }
};
</script>
