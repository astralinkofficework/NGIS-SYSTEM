# NGIS — New Gateway International School Portal

A clean, professional 2026 school management portal. Zero-build static site: open `index.html` in any browser.

## Quick Start

### Running the Server

This project uses Python Flask for the backend server:

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the server:**
   ```bash
   python server.py
   ```

   Or using npm scripts:
   ```bash
   npm start
   ```

3. **Access the application:**
   - Main portal: http://localhost:3000
   - Admin: http://localhost:3000/pages/admin/admin.html
   - Teacher: http://localhost:3000/pages/teacher/teacher.html
   - Student: http://localhost:3000/pages/student/student.html
   - Parent: http://localhost:3000/pages/parent/parent.html

The server runs on port 3000 by default. You can change this by setting the `PORT` environment variable:
```bash
PORT=8080 python server.py
```

## Structure

```
index.html              Landing — portal selector
{role}.html             Dashboards: admin, teacher, student, parent
{role}-{section}.html   36 sub-pages (users, classes, timetables, fees,
                        grades, attendance, assignments, announcements,
                        calendar, documents, notifications, profile, …)
assets/css/app.css      Single design system (tokens, components, responsive)
assets/js/layout.js     Layout engine — injects sidebar, topbar, bottom nav,
                        breadcrumb from window.PAGE = {role, active}
assets/js/app.js        Interactive layer (search, sort, attendance, grades)
```

Every page declares `window.PAGE = {role, active}` then loads `layout.js`,
which renders shared chrome and pulls in `app.js`. To add a page, copy an
existing sub-page, set `window.PAGE`, and link it from the nav config in
`layout.js`.

## Design system

Single source of truth in `assets/css/app.css` via CSS custom properties.

- **Primary** `#2563EB` · **Secondary** `#0F172A` · **Surface** `#FFFFFF` / `#F8FAFC`
- **Semantic** success `#16A34A` · warning `#F59E0B` · error `#DC2626`
- One accent (blue). Role identity is carried by icon + label, not color.
- Solid fills only — no gradients, no charts, no decorative graphics.
- Type: Inter. Headings 28–36, body 15–17. Radius 8–10px. Soft shadows.
- Motion 150–250ms, respects `prefers-reduced-motion`.

## Responsive & accessibility

- Desktop: left sidebar. Mobile (≤760px): off-canvas drawer + fixed bottom
  nav (Home / Classes-Schedule / Tasks / Alerts / Profile), 48px touch
  targets, safe-area insets.
- No horizontal scroll 320–1920px.
- Keyboard nav, visible focus rings, ARIA labels, `aria-current`, ⌘K search,
  Esc-to-close drawer, `.sr-only` helpers.

## Dark mode & language

Topbar toggles persist via the inline restore script in each page `<head>`.

## Notes

Fonts (Inter, Material Symbols) load from Google's CDN — an internet
connection is needed for icon glyphs and the Inter typeface; otherwise the
browser falls back to a system sans-serif.

## API Endpoints

The Flask server provides the following REST API endpoints:

### Health Check
- `GET /api/health` - Server health status

### News
- `GET /api/news` - Get all news (supports filtering by audience, priority, category, search)
- `GET /api/news/:id` - Get specific news item
- `POST /api/news` - Create news item
- `PUT /api/news/:id` - Update news item
- `DELETE /api/news/:id` - Delete news item

### Notifications
- `GET /api/notifications` - Get notifications (supports userId filter)
- `PUT /api/notifications/:id/read` - Mark notification as read
- `PUT /api/notifications/read-all` - Mark all notifications as read

### Students
- `GET /api/students` - Get all students
- `GET /api/students/:id` - Get specific student

### Clubs
- `GET /api/clubs` - Get all clubs
- `POST /api/clubs/:id/join` - Join a club

### Lost & Found
- `GET /api/lost-found` - Get lost & found items (supports type, status filters)
- `POST /api/lost-found` - Create lost & found entry

### Competitions
- `GET /api/competitions` - Get all competitions
- `POST /api/competitions/:id/register` - Register for competition

### Certificates
- `GET /api/certificates` - Get all certificates
- `GET /api/certificates/verify/:code` - Verify certificate by code

### Elections
- `GET /api/elections` - Get all elections
- `POST /api/elections/:id/vote` - Vote in election

### Feedback
- `POST /api/feedback` - Submit feedback

### Service Requests
- `GET /api/service-requests` - Get service requests (supports filters)
- `GET /api/service-requests/:id` - Get specific service request
- `POST /api/service-requests` - Create service request
- `PUT /api/service-requests/:id` - Update service request
- `DELETE /api/service-requests/:id` - Delete service request

### Projects
- `GET /api/projects` - Get all projects
- `PUT /api/projects/:pid/tasks/:tid` - Update project task

### Dashboard
- `GET /api/dashboard/:role` - Get dashboard summary for role (student, admin, etc.)

## Project Structure

```
index.html                    Landing page - portal selector
pages/
  admin/                      Admin portal pages
  teacher/                    Teacher portal pages
  student/                    Student portal pages
  parent/                     Parent portal pages
  shared/                     Shared pages (departments, chat, announcements, etc.)
assets/
  css/                        Stylesheets
  js/                         JavaScript files
server.py                     Flask server (Python)
requirements.txt              Python dependencies
package.json                 Project metadata
README.md                     This file
```
