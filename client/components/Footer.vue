<template>
  <footer class="footer text-white">
    <div>
      <p class="lead px-5">
        {{ new Date().getFullYear() }} - Crypto Candle Data
      </p>
    </div>
    <div>
      <ul>
        <li>
          <NuxtLink to="/terms-and-conditions"> Terms and Conditions </NuxtLink>
        </li>
        <li>
          <NuxtLink to="/privacy-policy"> Privacy Policy </NuxtLink>
        </li>
      </ul>
    </div>
    <div>
      <a class="px-5 text-underline-hover" href="mailto: cryptocandledata@gmail.com">
        cryptocandledata@gmail.com
      </a>
    </div>
  </footer>
</template>

<script>
export default {};
</script>

<style>
a {
  color: inherit;
  text-decoration: none;
}

a:hover {
  color: inherit;
  text-decoration: underline;
}
</style>
