import { Link, useLocation, useNavigate } from 'react-router-dom'

import { clearAccessToken, isAuthenticated } from '../services/auth'

function Navbar() {
  const location = useLocation()
  const navigate = useNavigate()
  const loggedIn = isAuthenticated()

  function handleLogout() {
    clearAccessToken()
    navigate('/login')
  }

  return (
    <header className="navbar">
      <div className="navbar__brand">Tasks App</div>
      <nav className="navbar__links">
        <Link className="nav-link" to="/dashboard">
          Dashboard
        </Link>
        {!loggedIn && (
          <>
            <Link className="nav-link" to="/login">
              {location.pathname === '/login' ? 'Login' : 'Sign in'}
            </Link>
            <Link className="button" to="/register">
              Create account
            </Link>
          </>
        )}
        {loggedIn && (
          <button className="button" type="button" onClick={handleLogout}>
            Logout
          </button>
        )}
      </nav>
    </header>
  )
}

export default Navbar