const express = require("express");

const app = express();

app.get("/", (req, res) => {

  res.send(`

  <!DOCTYPE html>
  <html>

  <head>

    <title>Sentinel Shield</title>

    <style>

      body{
        background:#0f172a;
        color:white;
        font-family:Arial;
        text-align:center;
        padding-top:100px;
      }

      .card{
        width:70%;
        margin:auto;
        background:#1e293b;
        padding:40px;
        border-radius:20px;
      }

      h1{
        color:#38bdf8;
        font-size:50px;
      }

      p{
        font-size:24px;
      }

    </style>

  </head>

  <body>

    <div class="card">

      <h1>🛡 Sentinel Shield</h1>

      <p>
      Predictive Intervention & Community Protection Network
      </p>

      <h2>✅ Website Running Successfully</h2>

    </div>

  </body>

  </html>

  `);

});

app.listen(5000, () => {
  console.log("Server running on port 5000");
});