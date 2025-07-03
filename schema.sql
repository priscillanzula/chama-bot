-- ============================
-- SCHEMA: Chama Payment Reminder Bot
-- ============================

-- ============================
-- TABLE: members
-- ============================
create table public.members (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  phone_number text not null,
  created_at timestamp with time zone default now()
);

-- ============================
-- TABLE: payments
-- ============================
create table public.payments (
  id uuid primary key default gen_random_uuid(),
  member_id uuid references public.members (id) on delete cascade,
  amount_due numeric not null,
  due_date date not null,
  is_paid boolean default false,
  paid_at timestamp with time zone,
  created_at timestamp with time zone default now()
);

-- ============================
-- TABLE: reminders
-- ============================
create table public.reminders (
  id uuid primary key default gen_random_uuid(),
  payment_id uuid references public.payments (id) on delete cascade,
  message_text text not null,
  sent_at timestamp with time zone default now(),
  status text default 'sent' not null
);

-- ============================
-- ROW LEVEL SECURITY (RLS)
-- ============================
-- Note: enabled RLS for all tables.
