const express = require("express");
const router = express.Router();
const Driver = require("../models/Driver");

// GET all drivers
router.get("/", async (req, res) => {
  try {
    const drivers = await Driver.find();
    res.json(drivers);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

// GET driver by driver_id
router.get("/driver-id/:driverId", async (req, res) => {
  try {
    const driver = await Driver.findOne({ driver_id: req.params.driverId });
    if (!driver) {
      return res.status(404).json({ message: "Driver not found" });
    }
    res.json(driver);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
});

module.exports = router;
