/**
 * NGIS — Audit log helper
 */

"use strict";

const { v4: uuidv4 } = require("uuid");

function writeAudit(db, { actorId, action, resource, resourceId, oldValue, newValue, ip }) {
  try {
    db.prepare(`
      INSERT INTO audit_logs (id, actor_id, action, resource, resource_id, old_value, new_value, ip_address)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    `).run(
      uuidv4(),
      actorId || null,
      action,
      resource,
      resourceId || null,
      oldValue ? JSON.stringify(oldValue) : null,
      newValue ? JSON.stringify(newValue) : null,
      ip || null
    );
  } catch (_) {
    // non-fatal
  }
}

module.exports = { writeAudit };
