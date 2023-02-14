<template>
  <div class="auth_wrapper auth">
    <div class="overlay"></div>
    <div class="cc_auth">
      <h2 class="title has-text-centered">Reset password</h2>

      <form method="post" @submit.prevent="resetPassword">
        <!-- <Notification :message="error" v-if="error" /> -->
        <div class="mb-3 mt-3">
          <p>
            Lost your password? Please enter your email address. You will
            receive a link to create a new password via email.
          </p>
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
        <button class="w-100 primary-btn" type="submit">Reset password</button>
      </form>
      <div class="d-flex align-items-center w-100 mt-2">
        <div class="divider"></div>
        <p class="m-0 m-2">or</p>
        <div class="divider"></div>
      </div>
      <div class="text-center">
        <p>
          <NuxtLink to="/login" class="">Login Here</NuxtLink>
        </p>
      </div>
    </div>
  </div>
</template>

<script>
// import Notification from '~/components/Notification'

export default {
  // middleware: 'guest',
  // components: {
  //     Notification,
  // },
  layout: "authlayout",
  data() {
    return {
      email: "",
      error: null,
    };
  },

  methods: {
    async resetPassword() {
      try {
        await this.$axios.post("reset-password", {
          email: this.email,
        });

        this.$notify({
          group: "auth",
          type: "success",
          title: "Success!",
          text: `Reset Mail Sent Successfully!`,
        });
        setTimeout(async () => {
          this.$router.push("/login");
        }, 1700);
      } catch (e) {
        this.$notify({
          group: "auth",
          type: "error",
          title: "Error!",
          text: "User (email) does not exists!",
        });
        console.log(e);
      }
    },
  },
};
</script>
