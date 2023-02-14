<template>
  <div class="auth-layout"><Nuxt /><Notify /></div>
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
};
</script>
