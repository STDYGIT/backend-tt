import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  {
    path: '/',
    component: () => import('../views/LandingView.vue'),
    meta: { guest: true },
  },
  {
    path: '/login',
    component: () => import('../views/auth/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/register',
    component: () => import('../views/auth/RegisterView.vue'),
    meta: { guest: true },
  },

  // ── User routes ──────────────────────────────────────────────
  {
    path: '/dashboard',
    component: () => import('../views/user/DashboardView.vue'),
    meta: { requiresAuth: true, role: 'user' },
  },
  {
    path: '/submit',
    component: () => import('../views/user/SubmitWasteView.vue'),
    meta: { requiresAuth: true, role: 'user' },
  },
  {
    path: '/my-entries',
    component: () => import('../views/user/MyEntriesView.vue'),
    meta: { requiresAuth: true, role: 'user' },
  },
  {
    path: '/entry/:id',
    component: () => import('../views/user/EntryDetailView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/profile',
    component: () => import('../views/user/ProfileView.vue'),
    meta: { requiresAuth: true },
  },

  // ── Admin routes ─────────────────────────────────────────────
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '', redirect: '/admin/dashboard' },
      { path: 'dashboard',   component: () => import('../views/admin/AdminDashboard.vue') },
      { path: 'entries',     component: () => import('../views/admin/AdminEntries.vue') },
      { path: 'entries/:id', component: () => import('../views/admin/AdminEntryDetail.vue') },
      { path: 'users',       component: () => import('../views/admin/AdminUsers.vue') },
      { path: 'users/:id',   component: () => import('../views/admin/AdminUserDetail.vue') },
      { path: 'categories',  component: () => import('../views/admin/AdminCategories.vue') },
      { path: 'zones',       component: () => import('../views/admin/AdminZones.vue') },
    ],
  },

  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

router.beforeEach((to) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return '/login'
  }
  if (to.meta.guest && auth.isLoggedIn) {
    return auth.isAdmin ? '/admin/dashboard' : '/dashboard'
  }
  if (to.meta.role === 'admin' && auth.isLoggedIn && !auth.isAdmin) {
    return '/dashboard'
  }
  if (to.meta.role === 'user' && auth.isLoggedIn && auth.isAdmin) {
    return '/admin/dashboard'
  }
})

export default router
