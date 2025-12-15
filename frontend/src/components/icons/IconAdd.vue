<template>
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <path 
      d="M12 5v14M5 12h14" 
      stroke="currentColor" 
      stroke-width="2" 
      stroke-linecap="round" 
      stroke-linejoin="round"
    />
  </svg>
</template>

<script setup>
defineProps({
  filled: {
    type: Boolean,
    default: false
  }
})
</script>

