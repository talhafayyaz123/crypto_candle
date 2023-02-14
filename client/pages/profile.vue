<template>
  <div class="profile">
    <Navbar />
    <div class="breadcrum">
      <div class="container">
        <h2>My Profile</h2>
      </div>
    </div>
    <div class="w-100 profile-nav mt-4 mb-5">
      <div class="container">
        <b-row>
          <b-col md="2" class="text-center">
            <div class="navbar-nav">
              <b-link v-on:click="displayHidden('account')" class="nav-item"
                >Account details</b-link
              >
              <b-link
                v-on:click="displayHidden('subscription')"
                class="nav-item"
                >My Subscription</b-link
              >
              <b-link v-on:click="displayHidden('apiKeys')" class="nav-item"
                >API Key</b-link
              >
            </div>
          </b-col>
          <b-col
            md="10"
            class="text-center"
            style="border-left: 1px solid #ccc"
          >
            <div v-if="account || placeholder">
              <p>
                <strong>Username:</strong>
                {{ user.username }}
              </p>
              <p>
                <strong>Email:</strong>
                {{ user.email }}
              </p>
            </div>
            <div v-else-if="subscription">
              <strong>Plan:</strong>
              {{ user.plan }}<br />

              <NuxtLink class="my-3 btn btn-primary" to="/pricing">
                Change plan
              </NuxtLink>
            </div>
            <div v-else-if="apiKeys">
              <strong>API Key:</strong>
              {{ user.apiKey }}<br />
              <b-button
                class="my-3"
                variant="outline-primary"
                @click="generateAPIKey()"
                >Generate new API Key</b-button
              >
              <p class="small">
                This will immediately revoke your current API key and display a
                new one here for you to copy.
              </p>
            </div>
          </b-col>
        </b-row>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import { mapActions, mapGetters } from "vuex";

export default {
  middleware: "auth",
  layout: "authlayout",
  data() {
    return {
      account: false,
      subscription: false,
      apiKeys: false,
      placeholder: true,
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
      attempt: "auth/attempt",
    }),

    async generateAPIKey() {
      await this.$axios.$get(`/generate-api-key?email=${this.user.email}`);
      await this.attempt(localStorage.getItem("USER_TOKEN"));
    },

    displayHidden(item) {
      this.placeholder = false;

      if (item == "account" && !this.account) {
        this.account = !this.account;
        this.subscription = false;
        this.apiKeys = false;
      } else if (item == "subscription" && !this.subscription) {
        this.account = false;
        this.apiKeys = false;
        this.subscription = !this.subscription;
      } else if (item == "apiKeys" && !this.apiKeys) {
        this.account = false;
        this.subscription = false;
        this.apiKeys = !this.apiKeys;
      }
    },
  },
};
</script>
