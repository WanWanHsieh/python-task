const BASE_URL = 'http://127.0.0.1:8000'

export interface Todo {
  id: number
  text: string
}

export async function getTodos(): Promise<Todo[]> {
  const res = await fetch(`${BASE_URL}/todos`)
  return res.json()
}

export async function addTodo(text: string): Promise<Todo> {
  const res = await fetch(`${BASE_URL}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
  return res.json()
}

export async function deleteTodo(id: number): Promise<void> {
  await fetch(`${BASE_URL}/todos/${id}`, { method: 'DELETE' })
}

export async function updateTodo(id: number, text: string): Promise<Todo> {
  const res = await fetch(`${BASE_URL}/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text }),
  })
  return res.json()
}


