const mongoose = require("mongoose");

const driverSchema = new mongoose.Schema(
  {
    driver_id: {
      type: String,
      required: true,
      unique: true,
    },
    name: {
      type: String,
      required: true,
    },
    phone_number: {
      type: String,
      required: true,
    },
    vehicle_id: {
      type: String,
      required: true,
    },
    lat: {
      type: Number,
      required: true,
    },
    long: {
      type: Number,
      required: true,
    },
    available: {
      type: Boolean,
      default: true,
    },
    status: {
      type: String,
      enum: ["free", "busy", "offline"],
      default: "free",
    },
    skills: [
      {
        type: String,
      },
    ],
    responded_count: {
      type: Number,
      default: 0,
    },
    rating: {
      type: Number,
      default: 0,
    },
    assigned_accident_id: {
      type: mongoose.Schema.Types.ObjectId,
      ref: "Accident",
    },
  },
  {
    timestamps: true,
  }
);

module.exports = mongoose.model("Driver", driverSchema);
