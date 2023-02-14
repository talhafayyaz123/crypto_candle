<template>
  <nav class="header navbar navbar-expand-lg"  ref="headRef">
    <div class="container">
      <!-- <a href="#" class="navbar-brand">Logo here</a> -->
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navmenu">
        <svg xmlns="http://www.w3.org/2000/svg" width="24px" height="24px" viewBox="0 0 24 24"><title>menu</title><path d="M3,6H21V8H3V6M3,11H21V13H3V11M3,16H21V18H3V16Z" /></svg>
      </button>
      <div class="sidebar-overlay has-dropdown is-hoverable collapse navbar-collapse" id="navmenu"
        data-bs-toggle="collapse" data-bs-target="#navmenu"></div>
      <div class="px-5 navbar-item has-dropdown is-hoverable collapse navbar-collapse drop-navbar" id="navmenu">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <NuxtLink to="/" class="nav-link"> Home </NuxtLink>
          </li>
          <!-- <li class="nav-item">
            <a href="/news" class="nav-link">News</a>
          </li> -->
          <li class="nav-item">
            <NuxtLink to="/pricing" class="nav-link"> Pricing </NuxtLink>
          </li>
          <li class="nav-item">
            <a href="https://documenter.getpostman.com/view/11410028/TVCY5BQc" class="nav-link" target="_blank">API
              Docs</a>
          </li>
          <li class="nav-item">
            <NuxtLink to="/candles" class="nav-link"> Get Candles </NuxtLink>
          </li>
          <li v-if="user && Object.keys(user).length > 0" class="nav-item dropdown">
            <button class="nav-btn" type="button" data-bs-toggle="dropdown"
              aria-expanded="false">
              {{ user.username }}
            </button>
            <ul class="dropdown-menu">
              <li>
                <NuxtLink to="/profile" class="dropdown-item text-decoration-none">
                  My Profile
                </NuxtLink>
                <button class="dropdown-item btn btn-primary" @click="logout">
                  Logout
                </button>
              </li>
            </ul>
          </li>
          <li v-else class="nav-item">
            <NuxtLink to="/login" class="nav-link log-btn">Login</NuxtLink>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  data() {
    return {
      isMenuOpen: false,
    };
  },
  computed: {
    ...mapGetters({
      authenticated: "auth/authenticated",
      user: "auth/user",
    }),
  },
  methods: {
    ...mapActions({
      logOut: "auth/logOut",
    }),

    async logout() {
      this.logOut();
    },
  },
  mounted(){
    var sticky = this.$refs['headRef'];
    window.addEventListener("scroll", () => {
        var curr = window.pageYOffset;

        if (curr >= 200) {
            sticky.classList.add("sticky");
        }else{
            sticky.classList.remove("sticky");
        }
    });
  },
};
</script>

<style scopped>
@media (max-width: 1000px) {
  .sidebar-overlay {
    position: fixed;
    width: 100%;
    height: 100%;
    left: 0;
    top: 0;
    background: #000;
    opacity: 0;
    z-index: 1050;
  }

  .navbar .navbar-toggler {
    z-index: 1060;
    position: relative;
  }

  .navbar .navbar-item {
    position: relative;
    z-index: 1060;
  }
}
</style>
