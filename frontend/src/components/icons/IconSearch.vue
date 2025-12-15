<template>
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle 
      cx="11" 
      cy="11" 
      r="8" 
      :stroke="filled ? 'none' : 'currentColor'"
      :fill="filled ? 'currentColor' : 'none'"
      stroke-width="2"
    />
    <path 
      d="M21 21l-4.35-4.35" 
      stroke="currentColor" 
      stroke-width="2" 
      stroke-linecap="round" 
      stroke-linejoin="round"
    />
    <circle 
      v-if="filled"
      cx="11" 
      cy="11" 
      r="4" 
      fill="var(--bg-dark, #0f0f23)"
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

