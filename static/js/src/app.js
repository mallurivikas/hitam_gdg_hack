// app.js
import { googleLogin, authListener } from "./auth.js";
import { saveUserToDB } from "./auth.js";

document.addEventListener('DOMContentLoaded', function() {
  const googleBtn = document.getElementById("googleBtn");

  if (googleBtn) {
    googleBtn.onclick = () => {
      googleLogin()
        .then(result => {
          saveUserToDB(result.user);
          console.log("Google user:", result.user);
          alert(`Welcome ${result.user.displayName}`);
        })
        .catch(err => alert(err.message));
    };
  }

  authListener((user) => {
    if (user) {
      saveUserToDB(user);
      console.log("Logged in:", user.email);
    } else {
      console.log("Logged out");
    }
  });
});
