export default function ({ store, redirect }) {
  console.log(".................11111111111111");
  if (store.getters["auth/authenticated"]) {
    return redirect("/");
  }
}
