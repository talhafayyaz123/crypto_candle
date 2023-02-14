<template lang="html">
  <client-only>
    <notifications
      group="auth"
      :duration="1500"
      :width="300"
      :speed="1000"
      animation-name="fade-left"
      position="top right"
    >
    </notifications>
  </client-only>
</template>
<script>
export default {
  name: "Notify",
};
</script>
