<template>
  <div class="fixed bottom-0 left-0 right-0 max-w-5xl w-full mx-auto bg-white border-t border-gray-100 px-6 py-2 pb-safe flex items-center justify-between z-40 shadow-[0_-4px_24px_rgba(0,0,0,0.04)]">
    <router-link to="/dashboard" class="flex flex-col items-center p-2 text-gray-400" active-class="text-primary-600">
      <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6" />
      </svg>
      <span class="text-[10px] font-semibold">Home</span>
    </router-link>

    <router-link to="/submit" class="flex flex-col items-center p-2 -mt-6">
      <div class="w-14 h-14 bg-primary-600 text-white rounded-full flex items-center justify-center shadow-[0_8px_16px_rgba(45,125,70,0.3)] hover:scale-105 active:scale-95 transition-transform">
        <svg class="w-7 h-7" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.5">
          <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4" />
        </svg>
      </div>
    </router-link>

    <router-link to="/my-entries" class="flex flex-col items-center p-2 text-gray-400" active-class="text-primary-600">
      <svg class="w-6 h-6 mb-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
        <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01" />
      </svg>
      <span class="text-[10px] font-semibold">Activity</span>
    </router-link>
  </div>
</template>

<style>
.pb-safe { padding-bottom: env(safe-area-inset-bottom, 0.5rem); }
</style>
