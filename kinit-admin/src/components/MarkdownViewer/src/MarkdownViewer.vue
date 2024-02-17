<script setup lang="ts">
import { ref, onMounted } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps({
  markdownContent: {
    type: String,
    required: true
  }
})

const parsedMarkdown = ref('')

onMounted(() => {
  const md = new MarkdownIt()
  parsedMarkdown.value = md.render(props.markdownContent)
})
</script>

<template>
  <div v-html="parsedMarkdown"></div>
</template>
