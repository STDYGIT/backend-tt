<template>
  <span :class="['status-' + status]">{{ icon }} {{ label }}</span>
</template>

<script setup>
const props = defineProps({ status: String })

const MAP = {
  pending:            { icon: '🟡', label: 'Pending' },
  under_verification: { icon: '🔍', label: 'Under Review' },
  verified:           { icon: '✅', label: 'Verified' },
  location_required:  { icon: '📍', label: 'Location Needed' },
  confirmed:          { icon: '✔️', label: 'Confirmed' },
  scheduled:          { icon: '📅', label: 'Pickup Scheduled' },
  completed:          { icon: '🚚', label: 'Completed' },
  rejected:           { icon: '❌', label: 'Rejected' },
}
const { icon, label } = MAP[props.status] || { icon: '❓', label: props.status }
</script>
