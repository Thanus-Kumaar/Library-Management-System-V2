<template>
  <div>
    <NavBar />

    <div class="d-flex flex-row p-4" style="margin-top: 10%;">
      <div class="d-flex flex-grow-1">
        <div class="mx-auto">
          <span class="display-2">Welcome {{ name }}</span>
          <span class="display-6 d-block">Library Management System</span>
        </div>
      </div>
      <div class="d-flex flex-fill">
        <div class="d-flex flex-column mx-auto row-gap-3">
          <button class="btn btn-light" type="button" @click="navigate('/manageBooks')">Manage Books</button>
          <button class="btn btn-light" type="button" @click="navigate('/manageSections')">Manage Sections</button>
          <button class="btn btn-light" type="button" data-bs-toggle="modal" data-bs-target="#UsersModal">View Users</button>
          <button class="btn btn-light" type="button" @click="navigate('/manageIssueRevoke')">Manage Issue / Revoke</button>
          <button class="btn btn-light" type="button" @click="navigate('/searchBooks')">Search Books</button>
        </div>
      </div>
    </div>

    <div class="modal" tabindex="-1" id="UsersModal" aria-labelledby="UsersModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Users</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <table class="table table-primary table-hover table-bordered table-responsive">
              <thead class="table-dark">
                <tr>
                  <th>User Name</th>
                  <th>Role</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(user, index) in userData" :key="index">
                  <td>{{ user[0] }}</td>
                  <td>{{ user[1] }}</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      name: 'User',
      userData: [
      ],
    };
  },
  methods: {
    navigate(path) {
      window.location.href = path;
    },
    getUserDetails(){
      axios.get("http://127.0.0.1:5000/getAllUserDetails")
      .then((response)=>{
        if(response.status == 200){
          console.log(response)
          this.userData = response.data["User Data"]
        }
      })
    }
  },
  created(){
    this.$checkUserRole("admin");
    this.getUserDetails();
  }
};
</script>
