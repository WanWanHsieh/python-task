<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTodos, addTodo, deleteTodo, updateTodo, type Todo } from '../api'

const todos = ref<Todo[]>([])
const newTodo = ref('')

async function loadTodos() {
  todos.value = await getTodos()
}

async function handleAdd() {
  if (!newTodo.value.trim()) return
  await addTodo(newTodo.value)
  newTodo.value = ''
  await loadTodos()
}

async function handleDelete(id: number) {
  await deleteTodo(id)
  await loadTodos()
}

const editingId = ref<number | null>(null)
const editingText = ref('')

function startEdit(todo: Todo) {
  editingId.value = todo.id
  editingText.value = todo.text
}

async function saveEdit(id: number) {
  if (!editingText.value.trim()) return
  await updateTodo(id, editingText.value)
  editingId.value = null
  await loadTodos()
}

onMounted(loadTodos)
</script>

<template>
  <main>
    <h1>待辦清單</h1>
    <input v-model="newTodo" @keyup.enter="handleAdd" placeholder="輸入待辦事項" />
    <button @click="handleAdd">新增</button>
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        <template v-if="editingId === todo.id">
          <input v-model="editingText" @keyup.enter="saveEdit(todo.id)" />
          <button @click="saveEdit(todo.id)">儲存</button>
        </template>
        <template v-else>
          {{ todo.text }}
          <button @click="startEdit(todo)">編輯</button>
          <button @click="handleDelete(todo.id)">刪除</button>
        </template>
      </li>
    </ul>
  </main>
</template>
