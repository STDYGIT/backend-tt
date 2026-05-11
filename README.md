# ♻️ TrashTreasure — Smart Waste Management System

TrashTreasure is a professional-grade waste management platform designed to connect environmentally conscious citizens with specialized recycling services. It bridges the gap between waste generation and responsible recycling through a seamless, automated digital experience.

---

## ✨ Key Features

### **For Users (Recyclers)**
- **Stateless Registration:** Secure, OTP-verified signup that prevents database pollution.
- **Waste Submission:** Categorize and submit waste entries (Plastic, Paper, Metal, E-waste) with photo evidence.
- **Live Status Tracking:** Monitor your pickup requests from "Pending" to "Collected".
- **Mobile Optimized:** Fully responsive UI for a smooth experience on smartphones.

### **For Admins / Recycling Companies**
- **Unified Dashboard:** View all pending collection entries with precise user details.
- **Entry Management:** Update pickup statuses and manage user records.
- **Role-Based Access:** Secure admin-only routes and actions protected by JWT.
- **Resource Management:** Manage Waste Categories and dynamic pricing/rules.

---

## 🛠️ Performance Tech Stack

### **Frontend Architecture**
- **Core:** Vue.js 3 with Vite for blazing-fast builds.
- **State:** Pinia (Store-based) for synchronized user sessions.
- **Routing:** Vue Router 4 with navigation guards.
- **Styles:** Tailwind CSS with a custom "Glassmorphism" theme.

### **Backend Infrastructure**
- **Logic:** Flask (Python) with a Modular Blueprint architecture.
- **Persistence:** PostgreSQL (Neon.tech) with optimized connection pooling.
- **Security:** PyJWT for stateless authentication and password hashing (Werkzeug).
- **Files:** Cloudinary CDN integration for lightning-fast image delivery.
- **Mail:** Resend HTTP API for reliable, port-block-proof OTP delivery.

---

## 🏗️ System Architecture & Engineering Logic

### **The Redirect-Proof Routing (Netlify)**
Since this is a Single Page Application (SPA), we use a `netlify.toml` file to redirect all traffic to `index.html`. This ensures that refreshing the page on routes like `/dashboard` doesn't lead to a 404.

### **Stateless OTP Protocol**
To prevent "Ghost Users" (unverified accounts) from filling our database, we use a token-relay system:
1. **Frontend** sends email ➔ **Backend** signs a JWT (otp_token) including the OTP ➔ **User** gets email.
2. **User** enters OTP ➔ **Backend** verifies JWT signature ➔ **Frontend** gets a `verified_token`.
3. Only when the user sets their password does the **Backend** create the actual database entry.

---

## 🚀 Deployment Specs

### **Render.com (Backend)**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Required Env Variables:**
  - `DATABASE_URL`: Your Neon Postgres URI.
  - `RESEND_API_KEY`: Your Resend.com API Key.
  - `MAIL_DEFAULT_SENDER`: Your verified domain email.
  - `CLOUDINARY_URL`: Your Cloudinary connection string.
  - `JWT_SECRET_KEY`: A strong random string for security.

### **Netlify (Frontend)**
- **Base directory:** `frontend`
- **Build command:** `npm run build`
- **Publish directory:** `dist`
- **Required Env Variables:**
  - `VITE_API_URL`: The URL of your Render backend.

---

## 👨‍💻 Post-Mortem: Lessons Learned
- **SMTP Limitations:** We learned that Render Free Tier blocks Port 587. Transitioning to the **Resend API** was the key to making the app production-ready.
- **Database Resilience:** We optimized SQLAlchemy for serverless PostgreSQL to prevent "unexpected EOF" errors by using `pool_pre_ping`.
- **Upload Optimization:** Increased Cloudinary timeouts to 60s to handle high-resolution image uploads from mobile devices.

---

## 👥 Contributors
Developed with a mission to clean the planet by **Jatin & Kamal**. 🌍
