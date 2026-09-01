/**
 * NGIS School ERP — Database Initialization
 * Creates the SQLite database and applies the schema.
 * Run: node backend/db/init.js
 */

"use strict";

const fs = require("fs");
const path = require("path");
const Database = require("better-sqlite3");

const DB_PATH = path.join(__dirname, "ngis.sqlite");
const SCHEMA_PATH = path.join(__dirname, "schema.sql");

console.log("══════════════════════════════════════════════");
console.log("  NGIS Database Initialization");
console.log("══════════════════════════════════════════════");

// Remove existing DB if --force flag is used
if (process.argv.includes("--force") && fs.existsSync(DB_PATH)) {
  fs.unlinkSync(DB_PATH);
  console.log("  ✓ Removed existing database");
}

const db = new Database(DB_PATH);

// Enable WAL mode for better concurrent performance
db.pragma("journal_mode = WAL");
db.pragma("foreign_keys = ON");

const schema = fs.readFileSync(SCHEMA_PATH, "utf8");
db.exec(schema);

console.log("  ✓ Schema applied successfully");
console.log(`  ✓ Database created at: ${DB_PATH}`);
console.log("══════════════════════════════════════════════\n");

db.close();
