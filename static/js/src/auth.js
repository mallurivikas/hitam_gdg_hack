// auth.js
import {
  onAuthStateChanged
} from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { doc, setDoc, getDoc } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";
import { db, auth } from "./firebase.js";

// Google Login
import { GoogleAuthProvider, signInWithPopup } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
const provider = new GoogleAuthProvider();


export const googleLogin = () =>
  signInWithPopup(auth, provider);

// Save user info in Firestore
export const saveUserToDB = async (user) => {
  try {
    
    // Reference to the user document
    const userRef = doc(db, "users", user.uid);

    // Get the document
    const userSnap = await getDoc(userRef);

    if (userSnap.exists()) {
      console.log("User already exists in DB:", userSnap.data());
      window.location.href = '/'; // Redirect to HTML page
    } else {
      // Create new user document
      await setDoc(userRef, {
        uid: user.uid,
        name: user.displayName || null,
        email: user.email,
        provider: user.providerData[0].providerId,
        createdAt: new Date().toISOString(),
      });
      console.log("New user saved to Firestore");
      window.location.href = '/assessment'; // Redirect to HTML page
    }
  } catch (err) {
    console.error("Error saving user to DB:", err);
  }
};

// Auth state listener
export const authListener = (callback) =>
  onAuthStateChanged(auth, callback);





