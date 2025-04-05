const mongoose = require("mongoose");

const ambulanceSchema = new mongoose.Schema({
  accidentID: String,
  PredictedClass: Number,
  body_parts: [String],
});

const Ambulance = mongoose.model("ambulance", ambulanceSchema);

module.exports = Ambulance;
