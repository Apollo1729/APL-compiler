<script setup lang="ts">
import { ref } from 'vue'
import OutputTabs from './components/OutputTabs.vue'
import axios from 'axios'
import CodeViewer from './components/CodeViewer.vue'
import AlertIcon from './components/AlertIcon.vue'
import CheckmarkIcon from './components/CheckmarkIcon.vue'
import { useToast } from 'vue-toast-notification'

// Reactive variables
const file = ref<File | null>(null)
const output = ref<string[]>([])
const error = ref<string>('')
const explanation = ref<string>('')
const tokens = ref<string[]>([])
const parseTree = ref<string>('')
const isLoading = ref(false)
const fileContent = ref<string>('')
const upload = ref(false)
const toast = useToast()

// Define button states
type ButtonState = 'idle' | 'loading' | 'success' | 'error'
const buttonState = ref<ButtonState>('idle')

// Handle file input change
const handleFileChange = (event: Event) => {
  fileContent.value = ''
  const target = event.target as HTMLInputElement
  file.value = target.files ? target.files[0] : null

  if (file.value) {
    const reader = new FileReader()
    reader.onload = (e) => {
      fileContent.value = e.target?.result as string
    }
    reader.readAsText(file.value)
  } else {
    fileContent.value = ''
  }

  console.log("from file: " + file.value)
}

// Handle form submission
const handleSubmit = async () => {
  if (!file.value) {
    toast.error('File is required to run the code.', {
      position: 'top-right',
      duration: 3000,
    })
    return
  }

  // Reset all outputs and state before uploading
  output.value = []
  error.value = ''
  explanation.value = ''
  tokens.value = []
  parseTree.value = ''
  upload.value = false
  buttonState.value = 'loading'

  isLoading.value = true

  try {
    await handleFileUpload()
    buttonState.value = 'success'
  } catch (err) {
    buttonState.value = 'error'
  } finally {
    isLoading.value = false
    setTimeout(() => {
      if (buttonState.value !== 'loading') {
        buttonState.value = 'idle'
      }
    }, 3000)
  }
}

// Handle file upload
const handleFileUpload = async () => {
  if (!file.value) return error.value = "Must have file content"

  try {
    const text = await file.value.text()
    console.log('File uploading')

    // Clear previous results
    output.value = []
    error.value = ''
    explanation.value = ''
    tokens.value = []
    parseTree.value = ''

    // Send the code content to the backend
    const response = await axios.post('https://compiler-dnekb9h7axggaxam.canadacentral-01.azurewebsites.net/compiler/compile', {
      code: text,
    })

    const result = response.data
    upload.value = true
    // Populate UI with real backend data
    output.value = (result.output || []).map((line: string) => line.trim())
    console.log(output)
    error.value = result.error || ''
    explanation.value = result.explanation || ''
    tokens.value = result.tokens || []
    parseTree.value = result.parseTree ? JSON.stringify(result.parseTree, null, 2) : ''
  } catch (err: any) {
    // Handle network or server errors
    const errorMessage = err.response?.data?.error
      || err.message
      || 'An unknown error occurred'

    error.value = `Failed to process file: ${errorMessage}`
    explanation.value = ''
    tokens.value = []
    parseTree.value = ''
  }
}


</script>

<template>
  <section
    class="min-h-screen h-screen overflow-auto p-10 lg:overflow-hidden lg:px-20 py-10 bg-stone-50 flex flex-col items-center">
    <h1 class="text-4xl text-center font-bold mb-8">Analysis of Programming Languages</h1>

    <div class="w-full flex flex-col h-1/2 lg:h-11/12 lg:flex-row gap-10 justify-center items-center">
      <!-- Card for File Upload -->
      <div class="bg-white w-full lg:w-1/2 shadow-lg rounded-lg p-6 flex flex-col h-full">
        <h2 class="font-bold text-xl mb-4">Uploaded Code File</h2>
        <CodeViewer :code="fileContent" />

        <label for="file-upload" class="font-semibold text-gray-700 mt-4">Upload Code File</label>
        <input type="file" id="file-upload" required @change="handleFileChange" accept=".txt,.code" class="text-sm lg:min-w-96 cursor-pointer text-stone-500 file:mr-4 file:py-2 file:px-4
          file:rounded file:border-0 file:text-sm file:font-semibold
          file:bg-blue-50 w-full file:text-blue-700 hover:file:bg-blue-100 disabled:bg-stone-300" />

        <!-- Submit Button -->
        <div class="mt-4 flex justify-center">
          <button @click="handleSubmit" :disabled="buttonState === 'loading'" :class="[
            'px-4 py-2 rounded-md font-medium cursor-pointer text-sm lg:w-56 flex items-center justify-center gap-2 transition-colors',
            {
              'bg-blue-600 hover:bg-blue-700 text-white': buttonState === 'idle',
              'bg-green-300 text-white': buttonState === 'success',
              'bg-red-600 text-white': buttonState === 'error',
              'bg-blue-300 text-gray-500 cursor-not-allowed': buttonState === 'loading'
            }
          ]">
            <span v-if="(buttonState === 'success' && upload)">
              <CheckmarkIcon />
            </span>
            <span v-else-if="buttonState === 'error'" class="flex items-center gap-2">
              <AlertIcon />
              <span>Try Again</span>
            </span>
            <span v-else-if="buttonState === 'loading'">
              <p>Processing...</p>
            </span>
            <span v-else>{{ buttonState === 'idle' ? 'Run Code' : 'Processing...' }}</span>
          </button>
        </div>
      </div>

      <!-- Output Section -->
      <div class="w-full lg:w-1/2 h-1/2 lg:h-full">
        <OutputTabs :output="output" :explanation="explanation" :tokens="tokens" :parse-tree="parseTree"
          :is-loading="isLoading" />
      </div>
    </div>
  </section>
</template>
