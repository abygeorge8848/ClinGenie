/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

//const {onRequest} = require("firebase-functions/v2/https");
//const logger = require("firebase-functions/logger");

// Create and deploy your first functions
// https://firebase.google.com/docs/functions/get-started

const express = require('express');
const router = express.Router();

router.use((req, res, next) => {
  console.log('Time: ', Date.now());
  next();
});

router.get('/', (req, res) => {
  res.send("Hello from the server!");
});

// Takes a query parameter, sends it to LangChain, and returns the response
router.post('/gptquery', async (req, res) => {
  const {query} = req.body;
  if (query !== undefined) {
    try {
      const chatdbchain = require("./chatdbchain.js");
      const resp = await chatdbchain.call({query});
      console.log('Issa me a luigio : ', resp);
      res.send(resp);
    } catch (error) {
      // logger.error(`Error getting GPT response: ${error}`);
      res.send({result: `Error getting GPT response: ${error}`});
    }
  } else {
    res.send("No query parameter provided");
  }
});



const sqlite3 = require('sqlite3').verbose();
const db = new sqlite3.Database('savedQueries.db', (err) => {
  if (err) {
    console.error(err.message);
  } else {
    console.log('Connected to the savedQueries database.');
  }
});

router.post('/save', async (req, res) => {
  const { query, result, sql } = req.body;
  if (result !== undefined) {
    db.run(`INSERT INTO entries (question, answer, sql_query) VALUES (?, ?, ?)`, 
    [query, result, sql], function (err) {
      if (err) {
        console.error(err.message);
        res.status(500).json({ error: 'Failed to save the data.' });
      } else {
        res.json({ message: 'Data saved successfully.' });
      }
    });

  } else {
    res.send("No result to be saved");
  }
});



router.get('/data', (req, res) => {
  const sql = 'SELECT id, answer, question, sql_query FROM entries';

  db.all(sql, [], (err, rows) => {
    if (err) {
      console.error(err.message);
      return res.status(500).json({ error: 'Failed to fetch data.' });
    }
    console.log('Ghey is : ', rows);
    res.json(rows);
  });
});



module.exports = router;
