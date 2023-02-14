<template>
  <div class="auth_wrapper auth">
    <div class="overlay"></div>
    <div class="cc_auth">
    <h2 class="title has-text-centered">Reset password</h2>

    <div v-if="validJWT == true">
      <form method="post" @submit.prevent="updatePassword">
        <p>Enter a new password below:</p>
        <div class="mb-3 mt-3">
          <label for="password" class="form-label">New password:</label>
          <input
            v-bind:type="[showPassword ? 'text' : 'password']"
            class="form-control"
            id="password"
            data-toggle="password"
            placeholder="Enter password"
            name="password"
            v-model="password"
            required
          />
          <input type="checkbox" @click="showPassword = !showPassword" /> Show
          password
        </div>
        <div class="mb-3 mt-3">
          <label for="password" class="form-label"
            >Re-enter new password:</label
          >
          <input
            v-bind:type="[showPassword ? 'text' : 'password']"
            class="form-control"
            id="password"
            placeholder="Enter password"
            name="password"
            v-model="passwordBis"
            required
          />
          <input type="checkbox" @click="showPassword = !showPassword" /> Show
          password
        </div>
        <div v-if="passwordsMatching == false">
          <b-alert show variant="danger">Passwords not matching</b-alert>
        </div>
        <b-button variant="outline-primary" type="submit">Save</b-button>
      </form>
    </div>
    <div v-else-if="validJWT == false">
      <b-alert show variant="danger">
        Reset password not successful. The link is invalid or has expired.
      </b-alert>
      <a class="btn btn-outline-primary" href="/" role="button"
        >Go to Homepage</a
      >
    </div>
  </div>
  </div>

</template>

<script>
export default {
  // middleware: 'guest',
  layout: "authlayout",
  data() {
    return {
      email: "",
      password: "",
      passwordBis: "",
      showPassword: false,
      resetPwdJWT: "",
      validJWT: null,
      passwordsMatching: null,
      error: null,
    };
  },

  computed: {
    buttonLabel() {
      return this.showPassword ? "Hide" : "Show";
    },
  },

  mounted() {
    this.resetPwdJWT = this.$route.query.token;
    this.verifyToken();
  },

  methods: {
    async verifyToken() {
      try {
        const res = await this.$axios.post("verify-JWT", {
          JWT: this.resetPwdJWT,
        });
        console.log(res.data);
        this.validJWT = res.data;
      } catch (e) {
        console.log(e);
      }
    },
    toggleShow() {
      this.showPassword = !this.showPassword;
    },
    checkPasswordsMatching() {
      if (this.password != this.passwordBis) {
        this.passwordsMatching = false;
      } else {
        this.passwordsMatching = true;
      }
    },
    async updatePassword() {
      this.checkPasswordsMatching();
      if (this.passwordsMatching) {
        try {
          await this.$axios.post("update-password", {
            resetPwdJWT: this.resetPwdJWT,
            password: this.password,
          });
          this.$router.push("/");
        } catch (e) {
          console.log(e);
        }
      }
    },
  },
};
</script>
