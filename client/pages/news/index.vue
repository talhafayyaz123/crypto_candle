<template>
  <div class="w-full h-full bg-primary">
    <section class="w-full h-96 bg-complementary relative">
      <div
        class="absolute bottom-0 w-full my-12 md:my-32 flex flex-col items-center z-10"
      >
        <h2
          class="text-4xl font-bold text-center mx-10 md:mx-40 my-8 text-primary-light"
        >
          Blog Posts
        </h2>
      </div>
    </section>
    <section id="generalSection" class="container ccdSection">
      <div class="columns is-5">
        <b-field class="column is-one-quarter" label="Filter:">
          <b-taginput
            v-model="selectedTags"
            :data="filteredTags"
            autocomplete
            :icon="selectedTags.length ? '' : 'label'"
            :placeholder="selectedTags.length ? '' : 'Search for tags'"
            rounded
            type="is-secondary has-text-primary-dark"
            @typing="getFilteredTags"
          >
          </b-taginput>
        </b-field>
        <b-field class="column" label="Order:">
          <b-select v-model="order" placeholder="Latest first">
            <option value="desc">Latest first</option>
            <option value="asc">Oldest first</option>
          </b-select>
        </b-field>
      </div>
      <div class="columns is-multiline is-5">
        <div
          v-for="article of filteredArticles"
          :key="article.slug"
          class="column is-one-third"
        >
          <div class="card has-background-primary-light has-text-primary-dark">
            <div class="card-image">
              <figure class="image is-4by3">
                <img :src="article.img" alt="Article image" />
              </figure>
            </div>
            <div class="card-content">
              <p class="title">
                <NuxtLink
                  :to="{ name: 'news-slug', params: { slug: article.slug } }"
                >
                  {{ article.title }}
                </NuxtLink>
              </p>
              <div class="content">
                <p>{{ article.description }}</p>
              </div>
            </div>
            <div class="card-footer">
              <time class="card-footer-item">{{
                new Date(article.createdAt).toLocaleDateString()
              }}</time>
              <p class="card-footer-item">
                <NuxtLink
                  :to="{ name: 'news-slug', params: { slug: article.slug } }"
                >
                  Read!
                </NuxtLink>
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script>
export default {
  async asyncData({ $content, params }) {
    const articles = await $content('articles', params.slug)
      .only([
        'title',
        'description',
        'tags',
        'img',
        'slug',
        'author',
        'createdAt',
      ])
      .sortBy('createdAt', 'desc')
      .fetch()

    const articleTags = [
      ...new Set(
        articles.reduce((acc, current) => [...acc, ...current.tags], [])
      ),
    ]
    return { articles, articleTags }
  },
  data() {
    return {
      filteredTags: this.articleTags,
      selectedTags: [],
      order: 'desc',
    }
  },
  computed: {
    orderedArticles() {
      return this.order === 'asc' ? [...this.articles].reverse() : this.articles
    },
    filteredArticles() {
      return this.selectedTags.length !== 0
        ? this.orderedArticles.filter((i) =>
            i.tags.some((t) => this.selectedTags.includes(t))
          )
        : this.orderedArticles
    },
  },
  methods: {
    getFilteredTags(text) {
      this.filteredTags = this.articleTags.filter((tag) =>
        tag.toLowerCase().includes(text.toLowerCase())
      )
    },
  },
}
</script>

<style scoped>
.ccdSection {
  padding-bottom: 50px !important;
}
</style>
