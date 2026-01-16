// Import from CDN - all imports must be consistent
import { initializeApp } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/10.7.1/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyAiWbU-URwjbTS3GcZcbvkvKyQaZIxpKNM",
  authDomain: "healthai-ac9ae.firebaseapp.com",
  projectId: "healthai-ac9ae",
  storageBucket: "healthai-ac9ae.firebasestorage.app",
  messagingSenderId: "54845894444",
  appId: "1:54845894444:web:f4237efd53c0ec6d5d4689",
  measurementId: "G-GMKJE3CT5H"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
export const auth = getAuth(app);
export const db = getFirestore(app);