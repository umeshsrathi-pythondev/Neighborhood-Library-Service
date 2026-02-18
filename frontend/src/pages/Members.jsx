import React, {useEffect, useState} from 'react'
import {api} from '../api'
import Notification from '../components/Notification'

export default function Members(){
  const [members, setMembers] = useState([])
  const [name, setName] = useState('')
  const [message, setMessage] = useState('')
  const [msgType, setMsgType] = useState('success')
  const [edited, setEdited] = useState({})

  useEffect(()=>{ api.members.list().then(setMembers).catch(console.error) }, [])

  const create = async ()=>{
    try{
      await api.members.create({name})
      setName('')
      const data = await api.members.list()
      setMembers(data)
      // initialize edited buffer
      const map = {}
      data.forEach(m=> map[m.id] = { name: m.name })
      setEdited(map)
      setMsgType('success'); setMessage('Member added')
    }catch(e){ setMsgType('danger'); setMessage(e.message) }
  }

  useEffect(()=>{ api.members.list().then(data=>{ setMembers(data); const map={}; data.forEach(m=> map[m.id]={name:m.name}); setEdited(map); }).catch(console.error) }, [])

  const applyUpdate = async (memberId)=>{
    try{
      const payload = edited[memberId]
      if(!payload) return
      await api.members.update(memberId, payload)
      const data = await api.members.list()
      setMembers(data)
      setEdited(prev=>({ ...prev, [memberId]: { name: data.find(d=>d.id===memberId).name } }))
      setMsgType('success'); setMessage('Member updated')
    }catch(e){ setMsgType('danger'); setMessage(e.message) }
  }

  return (
    <div className="container">
      <h2 className="my-4">Members</h2>
      <Notification message={message} type={msgType} onClose={()=>setMessage('')} />
      <div className="card p-3 mb-2">
        <div className="mb-2">
          <label className="form-label">Name</label>
          <input className="form-control" placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        </div>
        <button className="btn btn-primary btn-lg" onClick={create}>Add</button>
      </div>

      {members.length>0 ? (
        <table className="table table-hover">
          <thead><tr><th>ID</th><th>Name</th><th>Action</th></tr></thead>
          <tbody>
            {members.map(m=> (
              <tr key={m.id}>
                <td>{m.id}</td>
                <td><input className="form-control form-control-sm" value={edited[m.id]?.name ?? m.name} onChange={e=>setEdited(prev=>({...prev, [m.id]: { name: e.target.value }}))} /></td>
                <td><button className="btn btn-sm btn-primary" onClick={()=>applyUpdate(m.id)}>Update</button></td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (<p>No members yet.</p>)}
    </div>
  )
}
