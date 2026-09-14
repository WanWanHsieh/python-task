<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getTodos, addTodo, deleteTodo, type Todo } from '../api'

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

onMounted(loadTodos)
</script>

<template>
  <main>
    <h1>待辦清單</h1>
    <input v-model="newTodo" @keyup.enter="handleAdd" placeholder="輸入待辦事項" />
    <button @click="handleAdd">新增</button>
    <ul>
      <li v-for="todo in todos" :key="todo.id">
        {{ todo.text }}
        <button @click="handleDelete(todo.id)">刪除</button>
      </li>
    </ul>
  </main>
</template>
