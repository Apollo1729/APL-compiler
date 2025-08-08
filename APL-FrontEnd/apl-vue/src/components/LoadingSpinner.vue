<template>
    <div v-show="show" class="inline-flex border items-center justify-center">
        <div class="w-5 h-5 border-2 border-blue-500 border-t-transparent rounded-full animate-spin"></div>
    </div>
</template>


<script setup lang="ts">
defineProps({
    show: {
        type: Boolean,
        required: true
    }
})
</script>