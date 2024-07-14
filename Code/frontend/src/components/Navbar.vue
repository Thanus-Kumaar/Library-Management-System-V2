<template>
  <nav
    class="navbar navbar-expand-lg"
    style="background-color: rgb(30, 30, 30)"
  >
    <div class="container-fluid">
      <a class="navbar-brand text-light" href="#">Library Management System V2</a>
      <button
        class="navbar-toggler"
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
            <a class="nav-link active text-light" aria-current="page" href="#">Home</a>
          </li>
          <li class="nav-item mt-1">
            <a class="nav-link text-light" href="#">Link</a>
          </li>
          <li class="nav-item">
            <a class="nav-link">
              <button class="btn btn-secondary">Sign In</button>
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
