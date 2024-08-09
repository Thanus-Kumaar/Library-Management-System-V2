<template>
  <div>
    <div class="d-flex flex-row p-4" style="margin-top: 10%;">
      <div class="d-flex flex-grow-1">
        <div class="mx-auto">
          <span class="display-2">Welcome {{ name }}</span>
          <span class="display-6 d-block">Library Management System</span>
        </div>
      </div>
      <div class="d-flex flex-fill">
        <div class="d-flex flex-column mx-auto row-gap-3">
          <button class="btn btn-light" type="button" @click="navigate('/read-books')">Read Books</button>
          <button class="btn btn-light" type="button" @click="navigate('/user-books')">Request / Return books</button>
          <button class="btn btn-light" type="button" @click="navigate('/search-books')">Search Books</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: localStorage.getItem('username'),
    };
  },
  methods: {
    navigate(path) {
      window.location.href = path;
    }
  }
};
</script>