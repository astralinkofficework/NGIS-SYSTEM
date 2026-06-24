-- ============================================================
--  NGIS Chat Module — Supabase PostgreSQL Schema
--  Run this in the Supabase SQL editor to set up the database.
-- ============================================================

-- Enable UUID generation
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- ── users ────────────────────────────────────────────────────
-- Mirror of Supabase Auth users with school-specific fields.
-- Populate via a trigger on auth.users or manually via admin.
CREATE TABLE IF NOT EXISTS users (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  auth_id    UUID UNIQUE,                          -- links to auth.users.id
  name       VARCHAR(255) NOT NULL,
  email      VARCHAR(255) UNIQUE NOT NULL,
  role       VARCHAR(20)  NOT NULL
               CHECK (role IN ('super_admin','admin','teacher','student','parent')),
  avatar     TEXT,
  status     VARCHAR(10)  NOT NULL DEFAULT 'offline'
               CHECK (status IN ('online','away','offline')),
  last_seen  TIMESTAMPTZ  NOT NULL DEFAULT NOW(),
  created_at TIMESTAMPTZ  NOT NULL DEFAULT NOW()
);

-- ── conversations ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS conversations (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  type       VARCHAR(20) NOT NULL DEFAULT 'direct'
               CHECK (type IN ('direct','support')),
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── participants ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS participants (
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  joined_at       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  last_read_at    TIMESTAMPTZ,
  PRIMARY KEY (conversation_id, user_id)
);

-- ── messages ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS messages (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
  sender_id       UUID          REFERENCES users(id) ON DELETE SET NULL,
  message         TEXT NOT NULL CHECK (char_length(message) <= 2000),
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── message_status ────────────────────────────────────────────
-- One row per (message, recipient) — tracks read receipts.
CREATE TABLE IF NOT EXISTS message_status (
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  user_id    UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  read_at    TIMESTAMPTZ,
  PRIMARY KEY (message_id, user_id)
);

-- ── attachments ───────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS attachments (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
  file_url   TEXT NOT NULL,
  file_type  VARCHAR(50),
  file_name  VARCHAR(255),
  file_size  INTEGER,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── notifications ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS notifications (
  id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  message         TEXT NOT NULL,
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
  read            BOOLEAN NOT NULL DEFAULT FALSE,
  created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- ── Performance indexes ───────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_messages_conv    ON messages(conversation_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_participants_usr ON participants(user_id);
CREATE INDEX IF NOT EXISTS idx_msg_status_msg   ON message_status(message_id);
CREATE INDEX IF NOT EXISTS idx_notif_user       ON notifications(user_id, read, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_users_role       ON users(role);

-- ── Row Level Security ────────────────────────────────────────
ALTER TABLE users          ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversations  ENABLE ROW LEVEL SECURITY;
ALTER TABLE participants   ENABLE ROW LEVEL SECURITY;
ALTER TABLE messages       ENABLE ROW LEVEL SECURITY;
ALTER TABLE message_status ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications  ENABLE ROW LEVEL SECURITY;

-- Policies: the Node server uses the service role key (bypasses RLS)
-- These policies protect direct client access.

CREATE POLICY "Auth users can read all users"
  ON users FOR SELECT
  USING (auth.role() = 'authenticated');

CREATE POLICY "Users can update their own status"
  ON users FOR UPDATE
  USING (auth_id = auth.uid());

CREATE POLICY "Users see their own conversations"
  ON conversations FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM participants
    WHERE conversation_id = conversations.id AND user_id = (
      SELECT id FROM users WHERE auth_id = auth.uid()
    )
  ));

CREATE POLICY "Users see their participations"
  ON participants FOR SELECT
  USING (
    user_id = (SELECT id FROM users WHERE auth_id = auth.uid())
    OR EXISTS (
      SELECT 1 FROM participants p2
      WHERE p2.conversation_id = participants.conversation_id
        AND p2.user_id = (SELECT id FROM users WHERE auth_id = auth.uid())
    )
  );

CREATE POLICY "Users see messages in their conversations"
  ON messages FOR SELECT
  USING (EXISTS (
    SELECT 1 FROM participants
    WHERE conversation_id = messages.conversation_id
      AND user_id = (SELECT id FROM users WHERE auth_id = auth.uid())
  ));

CREATE POLICY "Users see their notifications"
  ON notifications FOR SELECT
  USING (user_id = (SELECT id FROM users WHERE auth_id = auth.uid()));

CREATE POLICY "Users can mark their notifications read"
  ON notifications FOR UPDATE
  USING (user_id = (SELECT id FROM users WHERE auth_id = auth.uid()));

-- ── Seed demo users (optional — remove in production) ─────────
-- INSERT INTO users (name, email, role) VALUES
--   ('Dr. Sarah Jenkins', 'sarah.jenkins@ngis.edu.kh', 'teacher'),
--   ('Kosal Rith Mony',   'kosal.mony@ngis.edu.kh',   'student'),
--   ('Chan Dara Vuth',    'chan.vuth@ngis.edu.kh',     'parent'),
--   ('Sok Panha Heng',    'sok.heng@ngis.edu.kh',      'admin');
