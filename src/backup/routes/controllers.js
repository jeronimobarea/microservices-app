const express = require('express');
const router = express.Router();

const admin = require("firebase-admin");

admin.initializeApp({
    credential: admin.credential.cert('./app-from-idea-to-code-firebase-adminsdk-ka5lc-a3a3a0665f.json')
});

const db = admin.firestore()


router.post('/', function (req, res, next) {
    let docRef = db.collection('app').doc('media');

    let setAda = docRef.set({
        "data" : req.body,
    });

    res.send(req.body)

});

module.exports = router;
