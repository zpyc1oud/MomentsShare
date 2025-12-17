<template>
  <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <template v-if="filled">
      <circle cx="12" cy="8" r="4" fill="currentColor"/>
      <path d="M20 21a8 8 0 10-16 0" fill="currentColor"/>
    </template>
    <template v-else>
      <circle 
        cx="12" 
        cy="8" 
        r="4" 
        stroke="currentColor" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
      />
      <path 
        d="M20 21a8 8 0 10-16 0" 
        stroke="currentColor" 
        stroke-width="2" 
        stroke-linecap="round" 
        stroke-linejoin="round"
      />
    </template>
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

