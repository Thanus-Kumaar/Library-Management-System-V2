<template>
  <nav
    class="navbar navbar-expand-lg mx-auto px-4 mt-3"
    style="background-color: rgba(40, 40, 50, 0.7); width: 60%; border-radius: 8px;"
  >
    <div class="container-fluid">
      <a class="navbar-brand text-light d-none d-lg-block" href="#">Library Management System V2</a>
      <button
        class="navbar-toggler "
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarSupportedContent"
        aria-controls="navbarSupportedContent"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarSupportedContent">
        <div class="me-auto"></div>
        <ul class="navbar-nav">
          <li class="nav-item mt-1">
            <router-link class="nav-link active text-light" to="/">Home</router-link>
          </li>
          <li class="nav-item mt-1">
            <router-link class="nav-link text-light">Link</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/login" class="nav-link">
              <button class="btn btn-secondary">Sign In</button>
            </router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
