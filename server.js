const express = require("express");
const mysql = require("mysql");
const cors = require("cors");
const app = express();
const db = require("./app/models/");

var corsOptions = {
  origin: "http://localhost:8000"
};

app.use(cors(corsOptions));

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// db.sequelize.sync();
db.sequelize.sync({ force: true }).then(() => {
  console.log("Drop and re-sync db.");
});

// const client = mysql.createConnection({
//   host: "localhost",
//   user: "tipotto",
//   password: "L1keana5234",
//   //   port: 3306,
//   database: "my_app"
// });

// const client =
//   process.env.NODE_ENV === "production"
//     ? mysql.createConnection({
//         user: process.env.REACT_APP_DB_USER,
//         password: process.env.REACT_APP_DB_PASSWORD,
//         database: process.env.REACT_APP_DB_DATABASE,
//         socketPath: `/cloudsql/${process.env.REACT_APP_INSTANCE_CONNECTION_NAME}`
//       })
//     : mysql.createConnection({
//         user: process.env.REACT_APP_DB_USER,
//         password: process.env.REACT_APP_DB_PASSWORD,
//         database: process.env.REACT_APP_DB_DATABASE,
//         host: "localhost"
//       });

// client.connect(err => {
//   if (err) {
//     console.error("error connecting: " + err.stack);
//     return;
//   }
//   console.log("connected as id " + client.threadId);
// });

// // read OK
// app.get("/user", (req, res) => {
//   client.query("SELECT * from users;", (err, rows, fields) => {
//     if (err) throw err;
//     res.send(rows);
//   });
// });

// // create ok
// app.post("/user/create", (req, res) => {
//   const name = req.body.username;
//   const email = req.body.email;
//   const password = req.body.password;

//   console.log("name: " + name);
//   console.log("email: " + email);
//   console.log("password: " + password);

//   client.query(
//     "INSERT INTO users SET ?",
//     { name: name, email: email, password: password },
//     (err, result) => {
//       if (err) res.send(err);

//       client.query(
//         "SELECT * from users WHERE email = ?",
//         [email],
//         (err, rows, fields) => {
//           if (err) res.send(err);
//           res.json({ data: rows });
//         }
//       );
//     }
//   );
// });

// update ok
// app.put("/user/update", (req, res) => {
//   const id = req.body.id;
//   const status = req.body.status;
//   client.query(
//     "UPDATE users SET status = ? WHERE id = ?",
//     [status, id],
//     (err, result) => {
//       if (err) throw err;
//       client.query("SELECT * from users;", (err, rows, fields) => {
//         if (err) throw err;
//         res.send(rows);
//       });
//     }
//   );
// });

// delete ok
// app.delete("/user/delete/", (req, res) => {
//   const id = req.query.id;
//   client.query(`DELETE FROM users WHERE id = ?`, [id], (err, result) => {
//     if (err) throw err;

//     client.query("SELECT * from users;", (err, rows, fields) => {
//       if (err) res.send(err);
//       res.json({ data: rows });
//     });
//   });
// });

require("./app/routes/user.routes")(app);

const PORT = process.env.PORT || 8080;
app.listen(PORT, () => console.log(`Server is running on port ${PORT}.`));
