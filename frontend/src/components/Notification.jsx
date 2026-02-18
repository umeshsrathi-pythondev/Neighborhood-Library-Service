import React from 'react';

export default function Notification({ message, type = 'success', onClose }) {
  if (!message) return null;
  return (
    <div className={`alert alert-${type} alert-dismissible fade show`} role="alert">
      {message}
      <button type="button" className="btn-close" aria-label="Close" onClick={onClose}></button>
    </div>
  );
}
