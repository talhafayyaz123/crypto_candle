/* eslint-disable prettier/prettier */
<template>
  <div class="bg-dark text-light text-center text-sm-start">
    <div class="breadcrum">
      <div class="container">
        <h2>Historical<span class="text-warning"> Cryptocurrency </span> Data</h2>
        <p class="lead my-4">
          Specify your parameters in the form below and get the candles in
          OHLC format (open, high, low, close).<br />
          Feel free to ask any question at
          <a class="has-text-secondary hover:underline" href="mailto: cryptocandledata@gmail.com">
            cryptocandledata@gmail.com
          </a>
        </p>
      </div>
    </div>
    <section class="mt-4">
      <div class="container">
        <h3>Select your desired exchange:</h3>
        <div class="candle-buttons mt-5 mb-5">
          <progress v-if="isLoadingExchanges" class="progress is-small is-dark" max="100"></progress>
          <div v-for="exchange in exchanges" v-else :key="exchange">
            <button class="candle-btn" :class="
              selectedExchange === exchange ? 'is-secondary' : 'is-light'
            " @click="getData(exchange)">
              <img style="width: 125px" :src="images[exchange.toLowerCase()]" :alt="`Logo of ${exchange}`" />
            </button>
          </div>
        </div>
      </div>
    </section>
    <section class="content ccdSection has-background-primary">
      <div class="container">
        <h3 class="title has-text-secondary">
          Select your crypto pair and interval:
        </h3>
        <progress v-show="selectedExchange && !pairs.length" class="progress is-small is-dark" max="100"></progress>
        <fieldset :disabled="!pairs.length" class="pt-5">
          <div class="row">
            <div class="col-md-4">
              <form>
                <div class="form-group">
                  <label>1. Start typing...</label>
                  <input v-model="inputSearch" class="form-control mt-3" :class="{ 'is-secondary': pairs.length }"
                    :placeholder="pairs.length ? 'e.g. BTC or ETH' : ''" />
                  <!-- <small id="emailHelp" class="form-text text-muted">We'll never share your email with anyone else.</small> -->
                </div>
              </form>
            </div>
            <div class="col-md-4">
              <label class="label is-6 has-text-primary-light">
                ... and choose your crypto pair</label>
              <select class="mt-3 form-select w-100" v-model="selectedPair">
                <option v-for="(pair, i) in searchPair" :key="i" :value="pair">
                  {{ pair }}
                </option>
              </select>
            </div>
            <div class="col-md-4">
              <label class="label is-6 has-text-primary-light">
                2. Set your interval</label>
              <select class="mt-3 form-select w-100" v-model="selectedInterval">
                <option v-for="(interval, i) in intervals" :key="i" :value="interval">
                  {{ interval }}
                </option>
              </select>
            </div>
          </div>
        </fieldset>
        <div class="text-center mt-4">
          <button class="primary-btn" @click="getCandle">
            Get your candles!
          </button>
        </div>
        <!-- Just to add a bit of space -->
        <div v-if="!candles" class="py-5"></div>
      </div>
    </section>

    <!-- <section class="px-5 py-3 content mb-0 ccdSection has-background-primary"> -->

    <section v-if="candles" class="bg-dark text-light mt-3 text-center text-sm-start">
      <div class="container">
        <div class="card bg-secondary text-light">
          <div class="card-body text-center">
            <div>
              <h5>
                <strong>Exchange:</strong>
                {{ candleExchange }}
              </h5>
            </div>
            <div>
              <h5>
                <strong>Pair:</strong>
                {{ candlePair }}
              </h5>
            </div>
            <div>
              <h5>
                <strong>Interval:</strong>
                {{ candleInterval }}
              </h5>
            </div>
          </div>
        </div>
        <div class="mt-3 mb-3">
          <button v-if="!isCopying" class="primary-btn" @click="copyCandles">
            Copy to clipboard
          </button>
          <button v-else class="primary-btn" @click="copyCandles">
            Copied to clipboard
          </button>
          <button class="primary-btn" @click="downloadCandles">Download</button>
        </div>
      </div>
    </section>
    <section v-else-if="isLoadingCandles" class="content ccdSection has-background-primary">
      <progress class="progress is-small is-dark" max="100"></progress>
    </section>
    <!-- Just to add a bit of space -->
    <div class="py-5"></div>
  </div>
</template>

<script>
const FileSaver = require("file-saver");
export default {
  // middleware: 'auth',
  data() {
    return {
      images: {
        binance: require("@/assets/images/binance.png"),
        kraken: require("@/assets/images/kraken.png"),
      },
      exchanges: [],
      inputSearch: "",
      pairs: [],
      intervals: [],
      candles: "",
      selectedExchange: "",
      selectedPair: "",
      selectedInterval: "",
      candleExchange: "",
      candlePair: "",
      candleInterval: "",
      isLoadingExchanges: false,
      isLoadingCandles: false,
      isCopying: false,
      service: "website",
    };
  },
  computed: {
    searchPair() {
      return this.pairs.filter((pair) =>
        pair.toLowerCase().includes(this.inputSearch.toLowerCase())
      );
    },
  },
  async mounted() {
    this.isLoadingExchanges = true;

    try {
      const { exchanges } = await this.$axios.$get(
        "https://cryptocandledata.com/api/exchanges"
      );

      this.exchanges = exchanges;
    } catch (e) {
      console.log(e);
    }

    this.isLoadingExchanges = false;
  },
  methods: {
    async getData(exchange) {
      this.selectedExchange = exchange;
      this.pairs = [];
      this.candles = "";
      this.selectedPair = "";
      this.selectedInterval = "";

      const { trading_pairs: tradingPairs } = await this.$axios.$get(
        `https://cryptocandledata.com/api/trading_pairs?exchange=${exchange}`
      );
      this.pairs = tradingPairs;

      const { intervals } = await this.$axios.$get(
        `https://cryptocandledata.com/api/intervals?exchange=${exchange}`
      );
      this.intervals = intervals;
    },
    getCandle() {
      this.candles = "";
      this.isLoadingCandles = true;

      this.candleExchange = this.selectedExchange;
      this.candlePair = this.selectedPair;
      this.candleInterval = this.selectedInterval;

      const startDate = "";
      const endDate = "";

      setTimeout(async () => {
        try {
          const { candles } = await this.$axios.$get(
            `https://cryptocandledata.com/api/candles?exchange=${this.selectedExchange}&tradingPair=${this.selectedPair}&interval=${this.selectedInterval}&startDateTime=${startDate}&endDateTime=${endDate}&service=${this.service}`
          );

          this.candles = candles;

          this.$notify({
            group: "auth",
            type: "success",
            title: "Success!",
            text: `Candles Successfully Fetched!`,
          });
        } catch (e) {
          this.$notify({
            group: "auth",
            type: "error",
            title: "Error!",
            text: "To Many Requests (5 per 1 minute)",
          });
          console.log(e);
        }
        this.isLoadingCandles = false;
      }, 1000);
    },
    getDate(date) {
      const year = date.getFullYear();
      const month = date.getMonth() + 1;
      const day = date.getDate();
      const hour = date.getHours();
      const minutes = date.getMinutes();
      const seconds = date.getSeconds();

      return `${year}-${month}-${day} ${hour}:${minutes}:${seconds}`;
    },
    copyCandles() {
      navigator.clipboard.writeText(JSON.stringify(this.candles));
      this.isCopying = true;
      setTimeout(() => (this.isCopying = false), 4000);
    },
    downloadCandles() {
      const blob = new Blob([JSON.stringify(this.candles)], {
        type: "text/plain;charset=utf-8",
      });

      FileSaver.saveAs(
        blob,
        `${this.selectedExchange}${this.selectedPair}${this.selectedInterval}.json`
      );
    },
  },
};
</script>

<style scoped>
.myBgImage {
  padding: 10% 10%;
}

.ccdContainer {
  background-color: #333533;
}

.headerSection {
  padding: 5% 0%;
}

.ccdResult {
  padding: 5% 0;
  border-radius: 10px;
  box-shadow: 0px 5px 10px gray;
}

.btnExchange {
  padding: 15px;
  margin: 5px;
  background-color: aliceblue;
  border: 2px solid darkgray;
}

.ccdSectionDisabled {
  background-color: black;
}
</style>
