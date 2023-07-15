const {DataSource} = require("typeorm");

const local = true; //Set this up to differentiate between local and cloud environments

/* const datasource = new DataSource({
  type: "postgres",
  host: local ? "127.0.0.1" : "/cloudsql/clingenie:us-central1:clingenie",
  port: local ? 4321 : 5432,
  username: "postgres",
  password: "root",
  database: "aramachandran",
  synchronize: true,
}); */

const datasource = new DataSource({
  type: "sqlite",
  database: "cgdb.sqlite",
  synchronize: true,
});

module.exports = {datasource};

// "/cloudsql/clingenie:us-central1:clingenie",
