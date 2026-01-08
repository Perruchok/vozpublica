"use client";

export default function ErrorBox({ message, onDismiss }) {
  return (
    <div className="error-box">
      <div className="error-content">
        <span className="error-icon">⚠️</span>
        <p className="error-message">{message}</p>
        {onDismiss && (
          <button
            className="dismiss-button"
            onClick={onDismiss}
            aria-label="Cerrar"
          >
            ✕
          </button>
        )}
      </div>
    </div>
  );
}
