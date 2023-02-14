<template>
  <section>
    <!-- Hero -->
    <div class="banner-section position-relative bg-dark text-light text-center text-sm-start">
      <div class="banner-content position-absolute top-50 start-50 translate-middle">
        <div class="py-5 my-5">
          <h1>Cryptocurrency<span class="text-warning"> market </span> data</h1>
          <p class="lead my-4">
            Useful for data analysis, trading & AI<br>
            - 100+ trading pairs<br>
            - Multiple exchanges supported<br>
            - All timeframes you need<br>
          </p>
          <NuxtLink class="primary-btn" to="/candles">
                Try it for free!
          </NuxtLink>
        </div>
      </div>

      <client-only>
        <Particles class="particles" color="#e8eddf" :particles-number="100" shape-type="polygon" :particle-size="3"
          movement-direction="top" lines-color="#e8eddf" :line-linked="true" :move-speed="0.75" :hover-effect="true" />
      </client-only>
    </div>

    <!-- Boxes -->
    <div class="pt-5 pb-5">
      <div class="container">
        <div class="row text-center g-4">
          <div class="col-md">
            <div class="card bg-dark text-light h-100">
              <div class="card-body text-center">
                <div class="h1 mb-3">
                  <i class="bi bi-laptop"></i>
                </div>
                <h3 class="card-title mb-3">Flexible historical data</h3>
                <p class="card-text">
                  You can download the cryptocurrency candlestick data directly from here or use our API. Whatever suits
                  you best!
                </p>
                <!-- TODO. Following button should go to a blog article explaining historical data -->
                <!-- <a href="#" class="btn btn-primary">Read More</a> -->
              </div>
            </div>
          </div>
          <div class="col-md">
            <div class="card bg-secondary text-light h-100">
              <div class="card-body text-center">
                <div class="h1 mb-3">
                  <i class="bi bi-person-square"></i>
                </div>
                <h3 class="card-title mb-3">Machine Learning</h3>
                <p class="card-text">
                  Train and test your Machine Learning models using real cryptocurrency candlestick data as datasets.
                </p>
                <!-- TODO. Following button should go to a blog article explaining ML application -->
                <!-- <a href="#" class="btn btn-dark">Read More</a> -->
              </div>
            </div>
          </div>
          <div class="col-md">
            <div class="card bg-dark text-light h-100">
              <div class="card-body text-center">
                <div class="h1 mb-3">
                  <i class="bi bi-people"></i>
                </div>
                <h3 class="card-title mb-3">Automated trading</h3>
                <p class="card-text">
                  Backtest your strategies with custom candlestick data (exchange, crypto pair, intervals…)
                </p>
                <!-- TODO. Following button should go to a blog article explaining automated trading -->
                <!-- <a href="#" class="btn btn-primary">Read More</a> -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- About -->
    <div id="learn" class="bg-dark text-light pt-5 pb-5">
      <div class="container">
        <div class="row align-items-center justify-content-between">
          <div class="col-md">
            <img
              src="https://images.unsplash.com/photo-1564503159823-a1b24c64a04f?ixlib=rb-1.2.1&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=891&q=80"
              class="img-fluid" alt="" />
          </div>
          <div class="col-md">
            <h2>About us</h2>
            <p class="lead">
              Crypto Candle Data started in the Netherlands back in 2020 as an indie project where developers from different countries collaborate along the way.
            </p>
            <p>
              The idea behind it is that we take into account the career preferences of the developers and adapt the project to them.
              If you think you can contribute to the project, just drop us an email at
              <a class="text-light fw-bold" href="https://mail.google.com/mail/?view=cm&fs=1&to=cryptocandledata@gmail.com"
                target="_blank">cryptocandledata@gmail.com</a>.
              The main goal is to ease the way for people to build something in the crypto space.<br>
              We'd love to see the cool stuff you can build with it!<br></br>
              Please no more duplicated work, use it people.<br>
              Seriously, do it.
            </p>
          </div>
        </div>
      </div>
    </div>


    <!-- Question Accordion -->
    <div id="questions" class="pb-5 pt-5">
      <div class="container">
        <h2 class="text-center mb-4">Frequently Asked Questions</h2>
        <div class="accordion accordion-flush" id="questions">
          <!-- Item 1 -->
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                data-bs-target="#question-one">
                What is Crypto Candle Data (CCD)?
              </button>
            </h2>
            <div id="question-one" class="accordion-collapse collapse" data-bs-parent="#questions">
              <div class="accordion-body">
                It's an interface between multiple crypto exchanges that allows you to fetch customized candle data without having to deal with specific exchange syntax.<br>
                Initially, we built it for ourselves because we needed it to test our trading and machine learning models with real and accurated data coming from the exchanges we use daily,
                but eventually we made it publicly available.
              </div>
            </div>
          </div>
          <!-- Item 2 -->
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                data-bs-target="#question-two">
                How can I interact with CCD?
              </button>
            </h2>
            <div id="question-two" class="accordion-collapse collapse" data-bs-parent="#questions">
              <div class="accordion-body">
                You can fetch the historical candle data using the website or (recommended) using the API where you can specify the time window you want.<br>
                Don't have an API-Key yet? Get it <a class="fw-bold" href="/profile">here</a>!
              </div>
            </div>
          </div>
          <!-- Item 3 -->
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                data-bs-target="#question-three">
                Is it free?
              </button>
            </h2>
            <div id="question-three" class="accordion-collapse collapse" data-bs-parent="#questions">
              <div class="accordion-body">
                Yes! We have a plan based pricing that fits different profiles (Free, Basic and Advanced) depending on the usage, however the Free plan has enough coverage to use the service.<br>
                Check the Pricing <a class="fw-bold" href="/pricing">here</a>!
              </div>
            </div>
          </div>
          <!-- Item 4 -->
          <div class="accordion-item">
            <h2 class="accordion-header">
              <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                data-bs-target="#question-four">
                What's in the roadmap?
              </button>
            </h2>
            <div id="question-four" class="accordion-collapse collapse" data-bs-parent="#questions">
              <div class="accordion-body">
                Expand horizontally by integrating more exchanges. At the moment we work with Binance and Kraken but there will be more coming soon.<br>
                Additionally, explore and carry out projects that new developers suggest!
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>
