export default function ({ store, redirect }) {
  if (store.state.auth.token === "null") {
    return redirect("/login");
  }
}
