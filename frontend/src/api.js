const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

async function request(path, opts){
  try{
    const res = await fetch(`${API_BASE}${path}`, opts)
    if(!res.ok){
      const txt = await res.text()
      throw new Error(txt || res.statusText)
    }
    return res.json()
  }catch(err){
    // network errors or CORS issues show up here
    console.error("API request failed", err)
    throw new Error(err.message || "network error")
  }
}

export const api = {
  books: {
    list: () => request('/books'),
    create: (payload) => request('/books', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) }),
    update: (id, payload) => request(`/books/${id}`, { method: 'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) }),
  },
  members: {
    list: () => request('/members'),
    create: (payload) => request('/members', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) }),
    update: (id, payload) => request(`/members/${id}`, { method: 'PUT', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) }),
  },
  loans: {
    list: (query='') => request(`/loans${query}`),
    borrow: (payload) => request('/loans/borrow', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) }),
    return: (payload) => request('/loans/return', { method: 'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify(payload) }),
  }
}
