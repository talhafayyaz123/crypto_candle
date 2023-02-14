<template>
  <div class="main-layout" ref="main_home">
    <Navbar />

    <Nuxt />
    <Notify />
    <Footer />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";
import Notify from "~/components/notify";
export default {
  data() {
    return {};
  },
  components: { Notify },
  computed: {
    ...mapGetters({
      authenticated: "auth/authenticated",
      user: "auth/user",
    }),
  },

  mounted() {
    this.keepUserLoggedIn();
  },

  methods: {
    ...mapActions({
      attempt: "auth/attempt",
    }),

    async keepUserLoggedIn() {
      await this.attempt(localStorage.getItem("USER_TOKEN"));
      console.log("default - ", this.user);
    },
  },
  // mounted() {
  //   this.$refs['main_home'].classList.add('main-home')
  //   console.log(this.$route)
  //   if(this.$route.name === 'index' ){
  //     this.$refs['main_home'].classList.add('main-home')
  //   }else{
  //     this.$refs['main_home'].classList.remove('main-home')
  //   }
  // },
};
</script>
