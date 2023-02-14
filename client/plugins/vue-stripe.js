import Vue from 'vue';
import { StripeCheckout } from '@vue-stripe/vue-stripe';
import { StripeElementCard } from '@vue-stripe/vue-stripe';

export default () => {
  Vue.component('StripeCheckout', StripeCheckout);
  Vue.component('StripeElementCard', StripeElementCard);
};