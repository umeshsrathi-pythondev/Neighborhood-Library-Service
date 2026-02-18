import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import Books from './pages/Books'
import Members from './pages/Members'
import Loans from './pages/Loans'
import Navbar from './components/Navbar'
import './styles.css'

function App(){
  return (
    <BrowserRouter>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<Books/>} />
          <Route path="/members" element={<Members/>} />
          <Route path="/loans" element={<Loans/>} />
        </Routes>
      </main>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App />)
