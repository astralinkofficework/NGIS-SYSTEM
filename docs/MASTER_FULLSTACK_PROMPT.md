MASTER FULL-STACK PROMPT — CONNECT ALL SCHOOL PORTALS

You are a senior full-stack engineer, software architect, UI/UX designer, database architect, and school ERP specialist.

I have an existing school management system with:

* Admin Portal
* Teacher Portal
* Student Portal
* Parent Portal

Your job is to audit and upgrade the ENTIRE SYSTEM — FRONTEND + BACKEND + DATABASE + API + AUTHENTICATION + AUTHORIZATION.

Do not only modify the frontend.

Do not only modify the backend.

Everything must work together as ONE connected school ERP.

⸻

1. FULL PROJECT AUDIT FIRST

Before making changes, inspect the entire repository.

Analyze:

FRONTEND

* Pages
* Components
* Layouts
* Sidebar/navigation
* Dashboard
* Forms
* Tables
* Modals
* Responsive design
* API calls
* State management
* Authentication handling
* Loading states
* Error states
* Empty states
* Permissions/UI visibility

BACKEND

* API routes
* Controllers
* Services
* Middleware
* Authentication
* Authorization
* Database queries
* Validation
* File uploads
* Notifications
* Messaging
* Error handling
* Logging
* Security

DATABASE

Identify:

* Tables/models
* Primary keys
* Foreign keys
* Relationships
* Indexes
* Constraints
* Duplicate data
* Missing relationships
* Incorrect relationships
* Orphaned records

INFRASTRUCTURE

Inspect:

* Environment variables
* Storage
* File handling
* API configuration
* CORS
* Authentication configuration
* Deployment configuration
* Database connection
* Production configuration

Do NOT guess how the application works.

Inspect the existing code and follow the existing architecture.

⸻

2. DO NOT REBUILD EVERYTHING

This is an existing project.

Do NOT rewrite the whole application unnecessarily.

Do NOT replace working functionality just because you prefer another architecture.

Instead:

1. Understand the current architecture.
2. Reuse existing components.
3. Reuse existing APIs where appropriate.
4. Reuse existing database tables where possible.
5. Fix broken relationships.
6. Add missing functionality.
7. Refactor only where necessary.

Preserve existing working features.

⸻

3. ONE SOURCE OF TRUTH

Admin, Teacher, Student and Parent must use the same backend/database.

Do NOT create separate duplicated databases or duplicated records for each portal.

Example:

DATABASE:

Student
↓
Class
↓
Subjects
↓
Teachers
↓
Assignments
↓
Submissions
↓
Grades

All portals read the appropriate information from this same data.

⸻

4. BACKEND ARCHITECTURE

Create a proper backend structure.

Use:

Frontend
↓
API
↓
Authentication Middleware
↓
Authorization / RBAC
↓
Controllers
↓
Services
↓
Database

Do NOT put all business logic inside frontend JavaScript.

Critical business rules must be enforced on the backend.

⸻

5. AUTHENTICATION

Implement secure authentication for:

* Admin
* Teacher
* Student
* Parent

The authenticated user must have a clear:

* user ID
* role
* account status
* permissions
* relationships

Never trust role information sent by the frontend.

The backend must determine the authenticated user’s identity and permissions.

⸻

6. ROLE-BASED ACCESS CONTROL

Implement proper RBAC.

Minimum roles:

ADMIN
TEACHER
STUDENT
PARENT

Every protected API endpoint must verify:

Authenticated User
→ Role
→ Relationship
→ Permission
→ Resource

Example:

GET /students/123/grades

The backend must verify whether the current user is actually allowed to access Student 123’s grades.

Do NOT rely on:

* hidden buttons
* hidden sidebar items
* frontend route protection
* URL obscurity

⸻

MOST IMPORTANT RULE

Do not treat the four portals as four independent websites.

Treat them as:

                SCHOOL ERP
                    │
          ┌─────────┴─────────┐
          │                   │
       DATABASE              API
          │                   │
 ┌────────┼────────┬──────────┤
 │        │        │          │

ADMIN   TEACHER  STUDENT    PARENT
│        │        │          │
MANAGE    TEACH    LEARN     MONITOR

The backend/database is the central source of truth.

The frontend is the role-specific interface.

Every module must connect through the backend.

Every permission must be enforced server-side.

Every relevant change must propagate to the correct portal.

Build this as a professional production-ready international-school ERP, not as four disconnected dashboards.
