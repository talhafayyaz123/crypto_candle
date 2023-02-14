export default {
  // Global page headers: https://go.nuxtjs.dev/config-head
  head: {
    title: "client",
    htmlAttrs: {
      lang: "en",
    },
    meta: [
      { charset: "utf-8" },
      { name: "viewport", content: "width=device-width, initial-scale=1" },
      { hid: "description", name: "description", content: "" },
      { name: "format-detection", content: "telephone=no" },
    ],
    link: [{ rel: "icon", type: "image/x-icon", href: "/favicon.ico" }],
  },

  // script: [
  //   { src: 'https://js.stripe.com/v3' },
  // ],

  // Global CSS: https://go.nuxtjs.dev/config-css
  css: ["~/assets/css/bootstrap.min.css", "~/assets/scss/style.css"],

  // Plugins to run before rendering page: https://go.nuxtjs.dev/config-plugins
  plugins: [
    { src: "~plugins/vueliate.js", ssr: false },
    { src: "~/plugins/bootstrap.js", mode: "client" },
    { src: "~/plugins/vue-stripe.js", ssr: false },
    { src: "~/plugins/vue-notification.js", ssr: false },
  ],
  target: "static",
  ssr: false,
  // Auto import components: https://go.nuxtjs.dev/config-components
  components: true,

  // Modules for dev and build (recommended): https://go.nuxtjs.dev/config-modules
  buildModules: [],
  /*  router: {
    middleware: ["guest"],
  }, */
  // Modules: https://go.nuxtjs.dev/config-modules
  modules: [
    // https://go.nuxtjs.dev/axios
    "@nuxtjs/axios",
    "bootstrap-vue/nuxt",
    "@nuxt/content",
  ],

  bootstrapVue: {
    icons: true,
  },

  // Axios module configuration: https://go.nuxtjs.dev/config-axios
  axios: {
    // Workaround to avoid enforcing hard-coded localhost:3000: https://github.com/nuxt-community/axios-module/issues/308
    baseURL: "http://localhost:5000",
  },

  // Build Configuration: https://go.nuxtjs.dev/config-build
  build: {},
};
