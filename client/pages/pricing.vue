<template>
  <div class="auth_wrapper">
    <Navbar />
    <div class="breadcrum">
      <div class="container">
        <h2>Pricing</h2>
      </div>
    </div>
    <div class="w-100 pricing-page mt-5">
      <stripe-checkout
        ref="checkoutRef"
        mode="subscription"
        :pk="publishableKey"
        :line-items="lineItems"
        :success-url="successURL"
        :cancel-url="cancelURL"
        @loading="(v) => (loading = v)"
      />
      <div class="container">
        <div class="row card-deck mb-3 text-center">
          <div class="col-md-4">
            <div class="card mb-4 box-shadow">
              <div class="card-header">
                <h4 class="my-0 font-weight-normal">Free</h4>
              </div>
              <div class="card-body">
                <h1 class="card-title pricing-card-title">
                  0$<small class="text-muted"></small>
                </h1>
                <ul class="list-unstyled mt-3 mb-4">
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    5 API calls/min
                  </li>
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    Frequently updated database
                  </li>
                  <li>
                    <b-icon icon="x-lg"></b-icon>
                    Email support
                  </li>
                </ul>
              </div>
              <div v-if="authenticated">
                <div class="card-footer bg-transparent">
                  <button disabled class="primary-btn">Current plan</button>
                </div>
              </div>
              <div v-else>
                <div class="card-footer bg-transparent">
                  <NuxtLink to="/signup" class="primary-btn">Sign up</NuxtLink>
                </div>
              </div>
            </div>
          </div>

          <!-- Basic Plan -->
          <div class="col-md-4">
            <div class="card mb-4 box-shadow">
              <div class="card-header">
                <h4 class="my-0 font-weight-normal">Basic</h4>
              </div>
              <div class="card-body">
                <h1 class="card-title pricing-card-title">
                  {{ prices?.Basic }}$<small class="text-muted">/ month</small>
                </h1>
                <ul class="list-unstyled mt-3 mb-4">
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    50 API calls/min
                  </li>
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    Frequently updated database
                  </li>
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    Basic email support
                  </li>
                </ul>
              </div>
              <div v-if="authenticated" class="card-footer bg-transparent">
                <button class="primary-btn">Select</button>
              </div>
              <div v-else class="card-footer bg-transparent">
                <NuxtLink to="/signup" class="primary-btn">Sign up</NuxtLink>
              </div>
            </div>
          </div>
          <!-- Advanced Plan -->
          <div class="col-md-4">
            <div class="card mb-4 box-shadow">
              <div class="card-header">
                <h4 class="my-0 font-weight-normal">Advanced</h4>
              </div>
              <div class="card-body">
                <h1 class="card-title pricing-card-title">
                  {{ prices?.Advanced }}$<small class="text-muted"
                    >/ month</small
                  >
                </h1>
                <ul class="list-unstyled mt-3 mb-4">
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    150 API calls/min
                  </li>
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    Frequently updated database
                  </li>
                  <li>
                    <b-icon icon="check-lg"></b-icon>
                    Priority email support
                  </li>
                </ul>
              </div>
              <div v-if="authenticated" class="card-footer bg-transparent">
                <button class="primary-btn">Select</button>
              </div>
              <div v-else class="card-footer bg-transparent">
                <NuxtLink to="/signup" class="primary-btn">Sign up</NuxtLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<script>
import { mapGetters } from "vuex";

export default {
  layout: "authlayout",
  data() {
    return {
      loading: false,
      publishableKey: "",
      lineItems: [],
      successURL: "https://cryptocandledata.com", // TODO. Create a payment success page
      cancelURL: "https://cryptocandledata.com",
      username: "",
      email: "",
      password: "",
      sessionId: "session-id", // session id from backend,
      prices: {},
    };
  },

  computed: {
    ...mapGetters({
      authenticated: "auth/authenticated",
      user: "auth/user",
    }),
  },

  async mounted() {
    /*  try {
      const prices = await this.$axios.get("pricing");
      this.prices = prices.data;
      const res = await this.$axios.get("config");
      this.publishableKey = res.data.publicKey;
    } catch (e) {
      console.log(e);
    } */
  },
  methods: {
    async selectPlan(plan) {
      if (!this.authenticated) {
        this.signup();
      }
      if (plan == "Basic") {
        const res = await this.$axios.get("stripe-line-items", {
          params: {
            plan: "Basic",
          },
        });
        this.lineItems = res.data;
      } else if (plan == "Advanced") {
        const res = await this.$axios.get("stripe-line-items", {
          params: {
            plan: "Advanced",
          },
        });
        this.lineItems = res.data;
      }
      console.log(this.lineItems);

      // Redirect to Stripe's secure checkout page
      this.$refs.checkoutRef.redirectToCheckout();
    },
  },
};
</script>

<style scoped>
/* .container {
  max-width: 960px;
} */
</style>
