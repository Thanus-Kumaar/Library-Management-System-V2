<template>
  <div class="text-light" style="padding-left: 100px; padding-right: 100px;">
    <Navbar />
    <Login />
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: "App",
};
</script>
