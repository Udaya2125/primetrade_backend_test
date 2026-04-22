import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import api from '../services/api'
import { setAccessToken } from '../services/auth'

function Login() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      const formData = new URLSearchParams()
      formData.set('username', email)
      formData.set('password', password)

      const response = await api.post('/auth/login', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      })
      setAccessToken(response.data.access_token)
      navigate('/dashboard')
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel hero">
      <h1>Sign in</h1>
      <form className="form" onSubmit={handleSubmit}>
        <input type="email" placeholder="Email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          maxLength={72}
          required
        />
        <button className="button" type="submit" disabled={loading}>
          {loading ? 'Signing in...' : 'Login'}
        </button>
      </form>
      {message && <p className="feedback">{message}</p>}
    </section>
  )
}

export default Login