const jwt = require("jsonwebtoken");
const supabase = require("../config/supabase");

// HTTP middleware — attaches req.user
async function requireAuth(req, res, next) {
  const auth = req.headers.authorization;
  if (!auth || !auth.startsWith("Bearer ")) {
    return res.status(401).json({ error: "Missing token" });
  }

  const token = auth.slice(7);
  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    const { data, error } = await supabase
      .from("users")
      .select("id,name,email,role,avatar,status")
      .eq("id", payload.userId)
      .single();

    if (error || !data) return res.status(401).json({ error: "User not found" });

    req.user = data;
    next();
  } catch {
    return res.status(401).json({ error: "Invalid or expired token" });
  }
}

// Socket.io middleware — attaches socket.user
async function socketAuth(socket, next) {
  const token = socket.handshake.auth?.token;
  if (!token) return next(new Error("AUTH_MISSING"));

  try {
    const payload = jwt.verify(token, process.env.JWT_SECRET);
    const { data, error } = await supabase
      .from("users")
      .select("id,name,email,role,avatar,status")
      .eq("id", payload.userId)
      .single();

    if (error || !data) return next(new Error("AUTH_USER_NOT_FOUND"));

    socket.user = data;
    next();
  } catch {
    next(new Error("AUTH_INVALID_TOKEN"));
  }
}

// Generate a JWT for a given userId (used at login)
function signToken(userId) {
  return jwt.sign({ userId }, process.env.JWT_SECRET, { expiresIn: "7d" });
}

module.exports = { requireAuth, socketAuth, signToken };
