require("dotenv").config();

const express = require("express");
const http    = require("http");
const cors    = require("cors");
const { Server } = require("socket.io");
const { socketAuth, signToken }    = require("./middleware/auth");
const { registerHandlers }         = require("./socket/handlers");
const { registerGroupHandlers }    = require("./socket/group-handlers");
const supabase                     = require("./config/supabase");

const app    = express();
const server = http.createServer(app);
const PORT   = process.env.PORT || 3001;
const ORIGIN = process.env.CLIENT_ORIGIN || "*";

// ── Middleware ────────────────────────────────────────────────
app.use(cors({ origin: ORIGIN, credentials: true }));
app.use(express.json({ limit: "1mb" }));

// ── Socket.io ─────────────────────────────────────────────────
const io = new Server(server, {
  cors: { origin: ORIGIN, methods: ["GET", "POST"] },
  pingTimeout: 30000,
  pingInterval: 10000,
});

io.use(socketAuth);

io.on("connection", (socket) => {
  console.log(`[socket] ${socket.user.name} (${socket.user.role}) connected`);
  registerHandlers(io, socket);
  registerGroupHandlers(io, socket);
});

// ── REST Routes ───────────────────────────────────────────────
app.use("/api/users",         require("./routes/users"));
app.use("/api/conversations", require("./routes/conversations"));
app.use("/api/messages",      require("./routes/messages"));
app.use("/api/classes",       require("./routes/classes"));

// Auth: issue a JWT token (call this from your school system login flow)
// POST /api/auth/token  { email, password }
app.post("/api/auth/token", async (req, res) => {
  const { email, password } = req.body;
  if (!email || !password) {
    return res.status(400).json({ error: "email and password required" });
  }

  // Authenticate via Supabase Auth
  const { data, error } = await supabase.auth.signInWithPassword({ email, password });
  if (error) return res.status(401).json({ error: "Invalid credentials" });

  // Find user in our users table
  const { data: user, error: userErr } = await supabase
    .from("users")
    .select("id,name,email,role,avatar")
    .eq("auth_id", data.user.id)
    .single();

  if (userErr || !user) {
    return res.status(404).json({ error: "User profile not found" });
  }

  const token = signToken(user.id);
  res.json({ token, user });
});

// Health check
app.get("/health", (_, res) => res.json({ status: "ok", ts: Date.now() }));

// ── Start ─────────────────────────────────────────────────────
server.listen(PORT, () => {
  console.log(`NGIS Chat Server running on port ${PORT}`);
  console.log(`Environment: ${process.env.NODE_ENV || "development"}`);
});
