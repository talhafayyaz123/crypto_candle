<template>
  <div class="auth_wrapper">
    <Navbar />
    <div class="pt-5 pb-5 h-100">
      <div class="container">
        <b-alert show variant="success"
          >A verification has been sent to your email. Please check also spam
          folder.</b-alert
        >
      </div>
    </div>
    <Footer />
  </div>
</template>
<script>
export default {
  layout: "authlayout",
};
</script>
