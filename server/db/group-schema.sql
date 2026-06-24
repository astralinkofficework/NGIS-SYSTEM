-- ============================================================
-- NGIS Group Chat Schema — Class-based group messaging
-- Run this AFTER the existing schema.sql (users table must exist)
-- Run in Supabase SQL editor
-- ============================================================

-- ── Classes ──────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS classes (
  id           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  name         TEXT NOT NULL,
  grade_level  TEXT,
  section      TEXT,
  description  TEXT,
  created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- ── Class members (who belongs to which class) ───────────────
CREATE TABLE IF NOT EXISTS class_members (
  id        UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  class_id  UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  user_id   UUID NOT NULL REFERENCES users(id)   ON DELETE CASCADE,
  role      TEXT NOT NULL CHECK (role IN ('teacher','student','parent','admin','super_admin')),
  joined_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(class_id, user_id)
);

-- ── Group messages ────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS group_messages (
  id         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  class_id   UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  sender_id  UUID REFERENCES users(id) ON DELETE SET NULL,
  message    TEXT NOT NULL CHECK (char_length(message) <= 2000),
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ── Read tracking (last read timestamp per user per class) ────
CREATE TABLE IF NOT EXISTS class_reads (
  class_id     UUID NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
  user_id      UUID NOT NULL REFERENCES users(id)   ON DELETE CASCADE,
  last_read_at TIMESTAMPTZ DEFAULT NOW(),
  PRIMARY KEY (class_id, user_id)
);

-- ── Performance indexes ───────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_group_messages_class
  ON group_messages(class_id, created_at DESC);

CREATE INDEX IF NOT EXISTS idx_class_members_user
  ON class_members(user_id);

CREATE INDEX IF NOT EXISTS idx_class_members_class
  ON class_members(class_id);

CREATE INDEX IF NOT EXISTS idx_class_reads_user
  ON class_reads(user_id);

-- ── Row Level Security ────────────────────────────────────────
ALTER TABLE classes        ENABLE ROW LEVEL SECURITY;
ALTER TABLE class_members  ENABLE ROW LEVEL SECURITY;
ALTER TABLE group_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE class_reads    ENABLE ROW LEVEL SECURITY;

-- Service role bypasses RLS (backend uses service key)
CREATE POLICY "service_all_classes"
  ON classes FOR ALL TO service_role USING (true);

CREATE POLICY "service_all_class_members"
  ON class_members FOR ALL TO service_role USING (true);

CREATE POLICY "service_all_group_messages"
  ON group_messages FOR ALL TO service_role USING (true);

CREATE POLICY "service_all_class_reads"
  ON class_reads FOR ALL TO service_role USING (true);

-- ── Seed demo data ────────────────────────────────────────────
-- Uncomment and adjust to seed initial classes:

-- INSERT INTO classes (id, name, grade_level, section) VALUES
--   ('00000000-0000-0000-0000-000000000001', 'Grade 7A',        'Grade 7', 'A'),
--   ('00000000-0000-0000-0000-000000000002', 'Grade 8B',        'Grade 8', 'B'),
--   ('00000000-0000-0000-0000-000000000003', 'Grade 9 Science', 'Grade 9', 'Science'),
--   ('00000000-0000-0000-0000-000000000004', 'Grade 10 Math',   'Grade 10','Math'),
--   ('00000000-0000-0000-0000-000000000005', 'Grade 11A',       'Grade 11','A'),
--   ('00000000-0000-0000-0000-000000000006', 'Grade 12 Science','Grade 12','Science')
-- ON CONFLICT (id) DO NOTHING;
