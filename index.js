// Import the functions you need from the SDKs you need
// const { initializeApp } = require("firebase/app");
// const { getAnalytics, isSupported } = require("firebase/analytics");
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

const express = require('express')
const app = express()
const port = 3000

//The static website is in the public folder
app.use(express.static('public'));

app.use(express.json());
app.use(express.urlencoded({ extended: true }));
const cg = require('./functions/index.js');
app.use('/cg', cg);


//Listen on port 3000
app.listen(port, () => {
  console.log(`ClinGenie app listening on port ${port}`)
})

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
/* const firebaseConfig = {
  apiKey: "AIzaSyB2cb8VlkkCYsko8ztmVVKZOG0c1Hw2v9Q",
  authDomain: "clingenie.firebaseapp.com",
  projectId: "clingenie",
  storageBucket: "clingenie.appspot.com",
  messagingSenderId: "100056471765",
  appId: "1:100056471765:web:69cb9ff1f4b656c2ce6a5c",
  measurementId: "G-V1VX032ZXM"
};
 */
// Initialize Firebase
/* const fbapp = initializeApp(firebaseConfig);
isSupported().then((isSupported) => {
  if (isSupported) {
    const analytics = getAnalytics(fbapp);
  }
}); */

