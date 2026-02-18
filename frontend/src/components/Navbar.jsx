import React, { useState } from 'react'
import { NavLink } from 'react-router-dom'

export default function Navbar(){
  const [open, setOpen] = useState(false)
  return (
    <header>
      <nav className="navbar navbar-expand-lg navbar-dark bg-primary">
        <div className="container-fluid">
          <div className="navbar-brand mb-0 h4">Neighborhood Library</div>
          <button className="navbar-toggler" type="button" onClick={()=>setOpen(o=>!o)} aria-label="Toggle navigation">
            <span className="navbar-toggler-icon" />
          </button>
          <div className={`collapse navbar-collapse ${open? 'show':''}`}>
            <ul className="navbar-nav me-auto mb-2 mb-lg-0">
              <li className="nav-item"><NavLink className={({isActive})=> isActive? 'nav-link active':'nav-link'} to="/">Books</NavLink></li>
              <li className="nav-item"><NavLink className={({isActive})=> isActive? 'nav-link active':'nav-link'} to="/members">Members</NavLink></li>
              <li className="nav-item"><NavLink className={({isActive})=> isActive? 'nav-link active':'nav-link'} to="/loans">Loans</NavLink></li>
            </ul>
          </div>
        </div>
      </nav>
    </header>
  )
}
