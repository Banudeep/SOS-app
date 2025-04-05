const express = require("express");
const router = express.Router();
const Ambulance = require("../models/Ambulance"); // Adjust the path as necessary

// GET route to fetch an accident by ID
router.get("/ambulance/:accidentID", async (req, res) => {
  try {
    console.log("In the backend", req.params);
    const { accidentID } = req.params;
    console.log("accidentID", accidentID);
    const document = await Ambulance.findOne({ accidentID: accidentID });

    if (document) {
      res.json(document);
    } else {
      res.status(404).send("document not found");
    }
  } catch (error) {
    console.error("Error:", error);
    res.status(500).send("Server error");
  }
});

module.exports = router;
