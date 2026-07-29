# Veterinary Clinic Management System - Project Plan

## Project Overview
Internal web application for veterinary clinic staff to manage patient records, visit history, and prescriptions. Built with Django + PostgreSQL, mobile-friendly design.

---

## Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| **Backend** | Django 5.x | Built-in auth, ORM, admin panel, excellent PostgreSQL support |
| **Database** | PostgreSQL | Robust, supports JSON fields for flexible data, audit-friendly |
| **Frontend** | Django Templates + Bootstrap 5 | Mobile-first, responsive, no JS framework needed |
| **CSS Framework** | Bootstrap 5 | Professional look, excellent mobile support on iOS/Android |
| **Icons** | Bootstrap Icons | Consistent professional appearance |
| **Hosting** | Hetzner Cloud | EU-based, affordable, professional grade |

---

## Core Features

### 1. User Management & Authentication
- Login/logout with session management
- Two roles: **Admin** (full access) and **Veterinarian** (medical access)
- Staff profiles: name, email, phone, role, specialization

### 2. Client (Pet Owner) Management
- Basic contact info: name, phone, email, address
- Link to all their pets
- Search by name/phone

### 3. Patient (Pet) Management
- **Basic Info**: name, species, breed, gender, date of birth, microchip number, photo
- **Audit-tracked fields**: weight history, age tracking with timestamps
- **Medical Info**: allergies, chronic conditions, notes
- Owner relationship (one owner → many pets)

### 4. Visit Management
- Visit date/time, reason for visit, attending veterinarian
- Visit status (scheduled, in-progress, completed)
- Links to: exam notes, prescriptions, lab results, files

### 5. Medical Records (per visit)
- **Exam Notes**: symptoms, diagnosis, treatment plan, follow-up notes
- **Manipulations**: procedures performed (e.g., blood draw, surgery, dental cleaning)
- **Vaccinations**: vaccine name, date administered, next due date, batch number
- **Prescriptions**: medication, dosage, frequency, duration, instructions
- **Lab Results**: uploaded files (PDF, images)
- **File Attachments**: X-rays, documents, any files

### 6. History Views
- Full visit history per patient
- Prescription history per patient
- Vaccination schedule/history
- Weight/measurement history with charts

---

## Database Schema

```
Users (Django built-in + extended)
├── role (admin/veterinarian)
├── phone, specialization

Clients (Pet Owners)
├── name, phone, email, address

Patients (Pets)
├── name, species, breed, gender, dob, microchip
├── photo, allergies, chronic_conditions
├── owner_id → Clients
│
├── WeightHistory (audit log)
│   ├── weight, recorded_at, recorded_by

Visits
├── patient_id → Patients
├── veterinarian_id → Users
├── date, reason, status, notes
│
├── ExamNotes
├── Manipulations
├── Vaccinations
├── Prescriptions
├── LabResults (file uploads)
├── Attachments (file uploads)
```

---

## Project Structure

```
vet_clinic/
├── manage.py
├── requirements.txt
├── requirements-prod.txt
├── .env.example
├── vet_clinic/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/          # User auth, profiles, roles
│   ├── clients/           # Pet owner management
│   ├── patients/          # Pet records, weight history
│   ├── visits/            # Visits, exams, prescriptions
│   └── core/              # Shared utilities, base templates
├── templates/
│   ├── base.html          # Main layout with navbar
│   ├── accounts/
│   ├── clients/
│   ├── patients/
│   └── visits/
├── static/
│   ├── css/
│   │   └── custom.css     # Green-white-brown theme
│   └── js/
├── media/                 # Uploaded files (lab results, attachments)
├── nginx.conf             # Nginx configuration
├── gunicorn.conf.py       # Gunicorn settings
└── deploy.sh              # Deployment script
```

---

## Color Theme (Green-White-Brown)

```css
:root {
    --primary-green: #2E7D32;      /* Main actions, navbar */
    --light-green: #81C784;        /* Hover states, accents */
    --white: #FFFFFF;              /* Backgrounds */
    --off-white: #F5F5F5;          /* Card backgrounds */
    --brown: #5D4037;              /* Text, headers */
    --light-brown: #8D6E63;        /* Secondary text */
}
```

---

## Mobile-First Approach

1. **Bootstrap 5 Grid System** - Responsive columns that stack on mobile
2. **Touch-friendly buttons** - Minimum 44px tap targets
3. **Collapsible navbar** - Hamburger menu on small screens
4. **Card-based layout** - Easy to read on any screen size
5. **Large form inputs** - Easy to use on touch devices
6. **Tested on**: iPhone Safari, Android Chrome

---

## Production Deployment (Hetzner)

### Infrastructure
| Component | Spec | Cost |
|-----------|------|------|
| Hetzner Cloud Server (CX21) | 2 vCPU, 4GB RAM, 40GB SSD | ~€5.50/mo |
| Hetzner Managed PostgreSQL | Basic tier | ~€10/mo |
| Hetzner Storage Box | 100GB for backups & uploads | ~€3/mo |
| Domain (Cloudflare) | .com | ~€9/year |
| **Total** | | **~€18-20/mo** |

### Server Stack
```
Nginx (reverse proxy, SSL termination)
    ↓
Gunicorn (WSGI application server)
    ↓
Django Application
    ↓
PostgreSQL (managed, with automatic backups)
```

### Security Configuration
- SSL/TLS via Let's Encrypt (free HTTPS)
- Nginx rate limiting
- Django CSRF protection
- Secure session cookies (HTTPS only)
- Database connections over private network
- Firewall: only ports 80, 443, 22 open
- Daily automated backups

---

## Implementation Phases

### Phase 1: Project Setup
- [ ] Initialize Django project with custom settings structure
- [ ] Configure PostgreSQL connection
- [ ] Set up project structure with apps
- [ ] Configure static files and media uploads
- [ ] Create base template with Bootstrap 5
- [ ] Apply green-white-brown color theme

### Phase 2: Authentication & Users
- [ ] Create custom user model with roles (Admin/Veterinarian)
- [ ] Build login/logout views
- [ ] Create staff profile management
- [ ] Implement role-based access control decorators

### Phase 3: Clients & Patients
- [ ] Create Client model and CRUD views
- [ ] Create Patient model with owner relationship
- [ ] Build WeightHistory audit model
- [ ] Implement patient search functionality
- [ ] Create client/patient list and detail views

### Phase 4: Visits & Medical Records
- [ ] Create Visit model and management views
- [ ] Build ExamNotes model and forms
- [ ] Create Manipulation records
- [ ] Implement Vaccination tracking with due dates
- [ ] Build Prescription model and history
- [ ] Create file upload for lab results and attachments

### Phase 5: History & Dashboard
- [ ] Create patient visit history view
- [ ] Build prescription history per patient
- [ ] Implement vaccination schedule view
- [ ] Add weight history chart (Chart.js)
- [ ] Create simple dashboard with recent activity

### Phase 6: Deployment Preparation
- [ ] Create production settings
- [ ] Write nginx.conf
- [ ] Create gunicorn.conf.py
- [ ] Write deployment script
- [ ] Create .env.example with all variables
- [ ] Document deployment steps

---

## Files to Create

### Core Project Files
1. `requirements.txt` - Development dependencies
2. `requirements-prod.txt` - Production dependencies
3. `.env.example` - Environment variables template
4. `manage.py` - Django management script

### Settings
5. `vet_clinic/settings/base.py` - Shared settings
6. `vet_clinic/settings/development.py` - Dev settings
7. `vet_clinic/settings/production.py` - Production settings
8. `vet_clinic/urls.py` - Main URL configuration
9. `vet_clinic/wsgi.py` - WSGI entry point

### Apps
10. `apps/accounts/` - User authentication app
11. `apps/clients/` - Client management app
12. `apps/patients/` - Patient management app
13. `apps/visits/` - Visit and medical records app
14. `apps/core/` - Shared utilities

### Templates
15. `templates/base.html` - Base template with Bootstrap
16. `templates/accounts/login.html` - Login page
17. `templates/clients/` - Client templates
18. `templates/patients/` - Patient templates
19. `templates/visits/` - Visit templates

### Static Files
20. `static/css/custom.css` - Custom theme styles

### Deployment
21. `nginx.conf` - Nginx configuration
22. `gunicorn.conf.py` - Gunicorn settings
23. `deploy.sh` - Deployment script

---

## Future Considerations (Not in scope now)
- Multi-clinic support (add Clinic model, link all records)
- Appointment scheduling/calendar
- Pet owner portal
- Inventory management
- SMS/Email notifications
- Reporting dashboard
