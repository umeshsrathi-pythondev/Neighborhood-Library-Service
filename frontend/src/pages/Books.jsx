import React, {useEffect, useState} from 'react'
import {api} from '../api'
import Notification from '../components/Notification'

export default function Books(){
  const [books, setBooks] = useState([])
  const [form, setForm] = useState({title:'', author:'', copies_total:1, copies_available:1})
  const [edited, setEdited] = useState({})
  const [message, setMessage] = useState('')
  const [msgType, setMsgType] = useState('success')

  useEffect(()=>{ api.books.list().then(data=>{ setBooks(data); const map = {}; data.forEach(b=> map[b.id]={copies_total:b.copies_total, copies_available:b.copies_available}); setEdited(map); }).catch(console.error) }, [])

  const create = async ()=>{
    try{
      await api.books.create(form)
      setForm({title:'', author:'', copies_total:1, copies_available:1})
      setBooks(await api.books.list())
      setMsgType('success'); setMessage('Book created successfully')
    }catch(e){ setMsgType('danger'); setMessage(e.message) }
  }

  const updateCopies = async (book, field, value)=>{
    // update local buffer only
    setEdited(prev=>({ ...prev, [book.id]: { ...(prev[book.id]||{}), [field]: Number(value) } }))
  }

  const applyUpdate = async (bookId)=>{
    try{
      const payload = edited[bookId]
      if(!payload) return
      await api.books.update(bookId, payload)
      const data = await api.books.list()
      setBooks(data)
      // refresh edited map for that book
      setEdited(prev=>({ ...prev, [bookId]: { copies_total: data.find(d=>d.id===bookId).copies_total, copies_available: data.find(d=>d.id===bookId).copies_available } }))
      setMsgType('success'); setMessage('Book updated')
    }catch(e){ setMsgType('danger'); setMessage(e.message) }
  }

  return (
    <div className="container">
      <h2 className="my-4">Books</h2>
      <Notification message={message} type={msgType} onClose={()=>setMessage('')} />
      <div className="card p-3 mb-4">
        <div className="mb-2">
          <label className="form-label">Title</label>
          <input className="form-control" placeholder="Title" value={form.title} onChange={e=>setForm({...form,title:e.target.value})} />
        </div>
        <div className="mb-2">
          <label className="form-label">Author</label>
          <input className="form-control" placeholder="Author" value={form.author} onChange={e=>setForm({...form,author:e.target.value})} />
        </div>
        <div className="mb-2">
          <label className="form-label">Copies Total</label>
          <input className="form-control" type="number" min="0" value={form.copies_total} onChange={e=>setForm({...form,copies_total:Number(e.target.value)})} />
        </div>
        <div className="mb-2">
          <label className="form-label">Copies Available</label>
          <input className="form-control" type="number" min="0" value={form.copies_available} onChange={e=>setForm({...form,copies_available:Number(e.target.value)})} />
        </div>
        <button className="btn btn-primary btn-lg" onClick={create}>Create</button>
      </div>

      {books.length > 0 ? (
        <table className="table table-striped">
          <thead><tr><th>ID</th><th>Title</th><th>Author</th><th>Available</th><th>Total</th></tr></thead>
          <tbody>
            {books.map(b=> (
              <tr key={b.id}>
                <td>{b.id}</td>
                <td>{b.title}</td>
                <td>{b.author}</td>
                <td><input className="form-control form-control-sm" type="number" value={edited[b.id]?.copies_available ?? b.copies_available} onChange={e=>updateCopies(b,'copies_available',e.target.value)} /></td>
                <td><input className="form-control form-control-sm" type="number" value={edited[b.id]?.copies_total ?? b.copies_total} onChange={e=>updateCopies(b,'copies_total',e.target.value)} /></td>
                <td><button className="btn btn-sm btn-primary" onClick={()=>applyUpdate(b.id)}>Update</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No books yet.</p>
      )}
    </div>
  )
}
