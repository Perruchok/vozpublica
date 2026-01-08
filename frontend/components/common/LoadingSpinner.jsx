"use client";

export default function LoadingSpinner({ message = "Cargando..." }) {
  return (
    <div className="loading-spinner">
      <div className="spinner"></div>
      <p className="loading-message">{message}</p>
    </div>
  );
}
