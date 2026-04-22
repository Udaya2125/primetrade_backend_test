import { useEffect, useState } from 'react'

import api from '../services/api'

function Dashboard() {
  const [tasks, setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  async function loadTasks() {
    setLoading(true)
    setMessage('')
    try {
      const response = await api.get('/tasks')
      setTasks(response.data)
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Unable to load tasks.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadTasks()
  }, [])

  async function handleCreateTask(event) {
    event.preventDefault()
    setMessage('')
    try {
      await api.post('/tasks', { title, description })
      setTitle('')
      setDescription('')
      setMessage('Task created.')
      await loadTasks()
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to create task.')
    }
  }

  async function handleToggle(task) {
    setMessage('')
    try {
      await api.patch(`/tasks/${task.id}`, { completed: !task.completed })
      await loadTasks()
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to update task.')
    }
  }

  async function handleDelete(taskId) {
    setMessage('')
    try {
      await api.delete(`/tasks/${taskId}`)
      setMessage('Task deleted.')
      await loadTasks()
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Failed to delete task.')
    }
  }

  return (
    <section className="grid">
      <div className="hero">
        <h1>Dashboard</h1>
        <p>Manage your tasks using the live API.</p>
      </div>

      <section className="panel">
        <h2 className="section-title">Create task</h2>
        <form className="form" onSubmit={handleCreateTask}>
          <input type="text" placeholder="Title" value={title} onChange={(event) => setTitle(event.target.value)} required />
          <textarea
            placeholder="Description"
            value={description}
            onChange={(event) => setDescription(event.target.value)}
          />
          <button className="button" type="submit">
            Add task
          </button>
        </form>
      </section>

      <section className="panel">
        <div className="row-between">
          <h2 className="section-title">Your tasks</h2>
          <button className="button" type="button" onClick={loadTasks} disabled={loading}>
            {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>

        {tasks.length === 0 && <p className="muted">No tasks yet.</p>}

        <div className="grid">
          {tasks.map((task) => (
            <article key={task.id} className="card task-card">
              <div>
                <h3 className="task-card__title">{task.title}</h3>
                <p className="task-card__meta">{task.description || 'No description'}</p>
                <p className="task-card__meta">Status: {task.completed ? 'Completed' : 'Open'}</p>
              </div>
              <div className="navbar__links">
                <button className="button" type="button" onClick={() => handleToggle(task)}>
                  {task.completed ? 'Mark open' : 'Mark done'}
                </button>
                <button className="button button-danger" type="button" onClick={() => handleDelete(task.id)}>
                  Delete
                </button>
              </div>
            </article>
          ))}
        </div>
      </section>

      {message && <p className="feedback">{message}</p>}
    </section>
  )
}

export default Dashboard