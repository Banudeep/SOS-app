const express = require("express");
const mongoose = require("mongoose");
const cors = require("cors");
require("dotenv").config();
//
const accidentRoutes = require("./routes/accidentRoutes");
const ambulanceRoutes = require("./routes/AmbulanceRoutes");
const driverRoutes = require("./routes/driverRoutes");
// check
const app = express();
app.use(
  cors({
    origin: true, // Allows all domains to access your resources
  })
);
app.use(express.json());
app.use(accidentRoutes);
app.use(ambulanceRoutes);
app.use(driverRoutes);

const MONGODB_URI =
  process.env.MONGODB_URI ||
  "mongodb+srv://banudeepreddy:Hello%40890@cluster0.m9gox.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0";
mongoose
  .connect(MONGODB_URI, { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("MongoDB Connected"))
  .catch((err) => console.error("MongoDB Connection Error:", err));

// app.use("/api", accidentRoutes);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(` Server running on port ${PORT}`));
