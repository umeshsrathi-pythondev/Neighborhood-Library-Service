import React, {useEffect, useState} from 'react'
import {api} from '../api'
import Notification from '../components/Notification'

export default function Loans(){
  const [loans, setLoans] = useState([])
  const [borrow, setBorrow] = useState({book_id:'', member_id:'', due_days:14})
  const [filterStatus, setFilterStatus] = useState('')
  const [message, setMessage] = useState('')
  const [msgType, setMsgType] = useState('success')

  const fetchLoans = async (status='') => {
    let query = ''
    if(status) query = `?status=${status}`
    const data = await api.loans.list(query)
    setLoans(data)
  }

  useEffect(()=>{ fetchLoans() }, [])

  const doBorrow = async ()=>{
    try{
      await api.loans.borrow({book_id: Number(borrow.book_id), member_id: Number(borrow.member_id), due_days: Number(borrow.due_days)})
      setBorrow({book_id:'', member_id:'', due_days:14})
      await fetchLoans(filterStatus)
      setMsgType('success'); setMessage('Book borrowed')
    }catch(e){ setMsgType('danger'); setMessage(e.message) }
  }

  const doReturn = async (loan_id)=>{
    try{
      await api.loans.return({loan_id})
      await fetchLoans(filterStatus)
      setMsgType('success'); setMessage('Book returned')
    }catch(e){ setMsgType('danger'); setMessage(e.message) }
  }

  return (
    <div className="container">
      <h2 className="my-4">Loans</h2>
      <Notification message={message} type={msgType} onClose={()=>setMessage('')} />
      <div className="card p-3 mb-2">
        <div className="mb-2">
          <label className="form-label">Book ID</label>
          <input className="form-control" placeholder="Book ID" value={borrow.book_id} onChange={e=>setBorrow({...borrow,book_id:e.target.value})} />
        </div>
        <div className="mb-2">
          <label className="form-label">Member ID</label>
          <input className="form-control" placeholder="Member ID" value={borrow.member_id} onChange={e=>setBorrow({...borrow,member_id:e.target.value})} />
        </div>
        <div className="mb-2">
          <label className="form-label">Due days</label>
          <input className="form-control" type="number" placeholder="Due days" value={borrow.due_days} onChange={e=>setBorrow({...borrow,due_days:Number(e.target.value)})} />
        </div>
        <button className="btn btn-primary btn-lg" onClick={doBorrow}>Borrow</button>
      </div>
      {/* filter */}
      <div className="mb-3">
        <label className="form-label">Status filter</label>
        <select className="form-select" value={filterStatus} onChange={e=>{setFilterStatus(e.target.value);fetchLoans(e.target.value)}}>
          <option value="">All</option>
          <option value="borrowed">Borrowed</option>
          <option value="returned">Returned</option>
        </select>
      </div>

      {loans.length>0 ? (
        <table className="table table-bordered">
          <thead><tr><th>ID</th><th>Book</th><th>Member</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            {loans.map(l=> (
              <tr key={l.id}>
                <td>{l.id}</td>
                <td>{l.book_id}</td>
                <td>{l.member_id}</td>
                <td>{l.status}</td>
                <td>{l.status==='borrowed' && <button className="btn btn-sm btn-secondary" onClick={()=>doReturn(l.id)}>Return</button>}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (<p>No loans found.</p>)}
    </div>
  )
}
