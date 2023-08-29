import React from "react";
import "./Loading.css"; // Import your custom CSS for styling

function Loading() {
  return (
    <div className="loading-container">
      <div className="loading-spinner">
        {/* Custom loading graphics */}
        <div className="spinner-border text-primary" role="status">
          <span className="sr-only">Loading...</span>
        </div>
        <p>Loading...</p>
      </div>
    </div>
  );
}

export default Loading;
