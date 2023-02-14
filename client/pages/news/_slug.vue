<template>
  <div class="has-background-primary myBgImage">
    <section class="hero is-medium-with-navbar is-primary">
      <div class="container hero-body">
        <div>
          <h1 class="title">{{ article.title }}</h1>
          <p>{{ article.description }}</p>
        </div>
      </div>
    </section>
    <article class="container cddArticle">
      <nuxt-content :document="article" />
    </article>
    <prev-next class="ccdPrevNext" :prev="prev" :next="next" />
  </div>
</template>

<script>
export default {
  async asyncData({ $content, params }) {
    const article = await $content('articles', params.slug).fetch()

    const [prev, next] = await $content('articles')
      .only(['title', 'slug'])
      .sortBy('createdAt', 'asc')
      .surround(params.slug)
      .fetch()

    return {
      article,
      prev,
      next,
    }
  },
  methods: {
    formatDate(date) {
      const options = { year: 'numeric', month: 'long', day: 'numeric' }
      return new Date(date).toLocaleDateString('en', options)
    },
  },
}
</script>

<style>
.myBgImage {
  padding: 10% 10% 5%;
}
.ccdContainer {
  background-color: #333533;
}
.cddArticle {
  margin-top: 5%;
  padding: 5%;
  border-radius: 10px;
  box-shadow: 0px 5px 10px gray;
  background-color: white;
}
.ccdPrevNext {
  padding: 5%;
}
.nuxt-content .icon-link {
  width: 0px;
}

.nuxt-content h1 {
  margin: 5% 0 2%;
  font-weight: bold;
  font-size: 32px;
}
.nuxt-content h2 {
  margin: 5% 0 2%;
  font-weight: bold;
  font-size: 28px;
}
.nuxt-content h3 {
  margin: 2% 2% 2%;
  font-weight: bold;
  font-size: 20px;
}
.nuxt-content p {
  margin: 0 0 2%;
}
.nuxt-content ul li {
  margin: 0 5%;
  list-style-type: disc;
}
</style>
