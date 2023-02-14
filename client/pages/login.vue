<template>
  <div class="auth_wrapper auth">
    <div class="overlay"></div>
    <!-- <Navbar /> -->
    <div class="cc_auth">
      <h2 class="title has-text-centered">Login</h2>

      <form method="post" @submit.prevent="submit">
        <!-- <Notification :message="error" v-if="error" /> -->

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
        <!-- <div class="form-check mb-3">
        <label class="form-check-label">
          <input class="form-check-input" type="checkbox" name="remember"> Remember me
        </label>
      </div> -->
        <button class="w-100 primary-btn" type="submit">Login</button>
      </form>
      <div class="d-flex align-items-center w-100 mt-2">
        <div class="divider"></div>
        <p class="m-0 m-2">or</p>
        <div class="divider"></div>
      </div>
      <div class="d-flex align-items-center justify-content-between w-100">
        <p>
          <NuxtLink to="/forgotPwd" class="">Forgot password?</NuxtLink>
        </p>
        <p>
          Don't have an account?
          <NuxtLink to="/signup" class="">Sign up</NuxtLink>
        </p>
      </div>
      <div class="divider mt-1"></div>
      <div class="mt-2">
        <NuxtLink to="/" class="">Back to home</NuxtLink>
      </div>
    </div>
    <!-- <Footer /> -->
  </div>
</template>

<script>
import { mapActions } from "vuex";
// import Notification from '~/components/Notification'
import { email, required } from "vuelidate/lib/validators";
import { validationMixin } from "vuelidate";
export default {
  middleware: "guest",
  // components: {
  //     Notification,
  // },
  layout: "authlayout",

  data() {
    return {
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
      logIn: "auth/logIn",
    }),

    submit() {
      const credentials = {
        email: this.email,
        password: this.password,
      };
      this.logIn(credentials)
        .then(() => {
          this.$notify({
            group: "auth",
            type: "success",
            title: "Success!",
            text: `Login Successfull!`,
          });

          this.$router.push("/profile");
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
