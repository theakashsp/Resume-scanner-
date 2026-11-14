// ==============================================================================
// TECH STACK: [Firebase Web Configuration]
// Reads configuration securely from environment variables (REACT_APP_FIREBASE_*)
// ensuring API keys and project credentials remain private and hidden from public Git.
// ==============================================================================

export const firebaseConfig = {
  apiKey: process.env.REACT_APP_FIREBASE_API_KEY || "",
  authDomain: process.env.REACT_APP_FIREBASE_AUTH_DOMAIN || "resume-scanner-ed200.firebaseapp.com",
  projectId: process.env.REACT_APP_FIREBASE_PROJECT_ID || "resume-scanner-ed200",
  storageBucket: process.env.REACT_APP_FIREBASE_STORAGE_BUCKET || "resume-scanner-ed200.firebasestorage.app",
  messagingSenderId: process.env.REACT_APP_FIREBASE_MESSAGING_SENDER_ID || "827724139699",
  appId: process.env.REACT_APP_FIREBASE_APP_ID || "1:827724139699:web:1ebd6780f35a9041bd74c6",
  measurementId: process.env.REACT_APP_FIREBASE_MEASUREMENT_ID || "G-VY85752PEK",
};

export const isFirebaseConfigured = () => {
  return Boolean(firebaseConfig.apiKey && firebaseConfig.projectId);
};

export default firebaseConfig;

