
export const state = () => ({
  token: "null",
  user: {},
});

export const mutations = {
  SET_TOKEN(state, token) {
    state.token = token;
  },
  SET_USER(state, data) {
    state.user = data;
  },
};

export const actions = {
  async signUp({ dispatch }, credentials) {
    console.log("store - signUp");
    console.log(credentials);
    let response = await this.$axios.post("signup", credentials);
    console.log(response.data);
    return dispatch("attempt", response.data);
  },

  async logIn({ dispatch }, credentials) {
    let response = await this.$axios.post("login", credentials);
    console.log("store - logIn " - response.data);
    return dispatch("attempt", response.data);
  },

  async attempt({ commit }, token) {
    console.log("store - attempt ");

    if (!token) {
      console.log("store - attempt - No token provided");
      commit("SET_USER", null);
      return;
    }

    commit("SET_TOKEN", token);

    try {
      let response = await this.$axios.get("me", {
        headers: {
          Authorization: "Bearer " + token,
        },
      });

      localStorage.setItem("USER_TOKEN", token);
      commit("SET_USER", response.data);
    } catch (error) {
      console.log("store - attempt - Something went wrong - ", error);
      commit("SET_TOKEN", null);
      commit("SET_USER", null);
    }
  },

  async logOut({ commit }) {
    let token = localStorage.getItem("USER_TOKEN");

    try {
      let response = await this.$axios.get("logout", {
        headers: {
          Authorization: "Bearer " + token,
        },
      });

      localStorage.removeItem("USER_TOKEN");
      commit("SET_TOKEN", null);
      commit("SET_USER", null);
      this.$router.push("/");
    } catch (error) {
      console.log("store - logOut - Something went wrong - ", error);
    }
  },
};

export const getters = {
  authenticated(state) {
    return state.token && state.user;
  },

  user(state) {
    return state.user;
  },
};
