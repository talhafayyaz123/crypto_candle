<template>
  <div class="auth_wrapper auth">
    <div class="overlay"></div>
    <div class="cc_auth">
      <h2 class="title has-text-centered">Sign up</h2>

      <form method="post" @submit.prevent="submit">
        <!-- <Notification v-if="error" :message="error" /> -->

        <div class="mb-3 mt-3">
          <label for="username" class="form-label">Username:</label>
          <input
            type="username"
            class="form-control"
            id="username"
            placeholder="Enter username"
            name="username"
            v-model="username"
            required
          />
        </div>
        <div class="mb-3 mt-3">
          <label for="email" class="form-label">Email:</label>
          <input
            type="email"
            class="form-control"
            id="email"
            placeholder="Enter email"
            name="email"
            v-model="email"
            required
          />
        </div>
        <div class="mb-3 mt-3">
          <label for="password" class="form-label">Password:</label>
          <input
            v-bind:type="[showPassword ? 'text' : 'password']"
            class="form-control"
            id="password"
            placeholder="Enter password"
            name="password"
            v-model="password"
            required
          />
          <input type="checkbox" @click="showPassword = !showPassword" /> Show
          password
        </div>
        <button class="primary-btn w-100" type="submit">Sign up</button>
      </form>
      <div class="d-flex align-items-center w-100 mt-2">
        <div class="divider"></div>
        <p class="m-0 m-2">or</p>
        <div class="divider"></div>
      </div>
      <div class="text-center">
        <p>
          Already have an account?
          <NuxtLink to="/login" class="">Login</NuxtLink>
        </p>
      </div>
      <div class="divider mt-1"></div>
      <div class="mt-2">
        <NuxtLink to="/" class="">Back to home</NuxtLink>
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from "vuex";
// import Notification from '~/components/Notification'

export default {
  // components: {
  //   Notification,
  // },
   middleware: 'guest',
  /* middleware({ store, redirect }) {
    if (process.client) {
      if (store.getters["auth/authenticated"]) {
        return redirect("/");
      }
    }
  }, */
  layout: "authlayout",
  data() {
    return {
      username: "",
      email: "",
      password: "",
      showPassword: false,
      error: null,
    };
  },

  computed: {
    buttonLabel() {
      return this.showPassword ? "Hide" : "Show";
    },
  },

  methods: {
    toggleShow() {
      this.showPassword = !this.showPassword;
    },

    ...mapActions({
      signUp: "auth/signUp",
    }),

    submit() {
      const credentials = {
        username: this.username,
        email: this.email,
        password: this.password,
      };
      this.signUp(credentials)
        .then(() => {
          this.$notify({
            group: "auth",
            type: "success",
            title: "Success!",
            text: `Signup Successfull`,
          });
          this.$router.push("/pendingEmailVerification");
        })
        .catch((err) => {
          this.$notify({
            group: "auth",
            type: "error",
            title: "Error!",
            text: err.response.data,
          });
          this.error = err.response;
        });
    },
  },
};
</script>
