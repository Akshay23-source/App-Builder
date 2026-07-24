import { initializeApp, getApps, getApp } from "firebase/app";
import { getAuth, GoogleAuthProvider, RecaptchaVerifier, signInWithPhoneNumber, signInWithPopup } from "firebase/auth";

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY || "mock-api-key",
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN || "forgeai-auth.firebaseapp.com",
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID || "forgeai-auth",
};

const app = !getApps().length ? initializeApp(firebaseConfig) : getApp();
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();

export const setupRecaptcha = (elementId: string) => {
  if (typeof window === "undefined") return null;
  return new RecaptchaVerifier(auth, elementId, {
    size: "invisible",
    callback: () => {
      // reCAPTCHA solved
    },
  });
};
