import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

import api from '../services/api'

function Register() {
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [message, setMessage] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setLoading(true)
    setMessage('')

    try {
      await api.post('/auth/register', {
        full_name: fullName,
        email,
        password,
      })
      setMessage('Registration successful. Please login.')
      navigate('/login')
    } catch (error) {
      setMessage(error?.response?.data?.detail || 'Registration failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <section className="panel hero">
      <h1>Create account</h1>
      <form className="form" onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Full name"
          value={fullName}
          onChange={(event) => setFullName(event.target.value)}
          required
        />
        <input type="email" placeholder="Email" value={email} onChange={(event) => setEmail(event.target.value)} required />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
          minLength={8}
          maxLength={72}
          required
        />
        <button className="button" type="submit" disabled={loading}>
          {loading ? 'Creating...' : 'Register'}
        </button>
      </form>
      {message && <p className="feedback">{message}</p>}
    </section>
  )
}

export default Register