import React from "react";
import { Link } from "react-router-dom";

function Home() {
  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100">
      <div className="card text-center w-50">
        <div className="card-body">
          <h2 className="card-title">Welcome to the S3 Dashboard</h2>
          {localStorage.getItem("secretAccessKey") ? (
            <div>
              <h3 className="card-subtitle mb-2 text-success">Logged In</h3>
              <p className="card-text">Welcome! You are logged in.</p>
              <Link to="/buckets" className="btn btn-primary">
                Show all bucket information
              </Link>
              <Link to="/objects" className="btn btn-secondary ml-2">
                Show all objects information
              </Link>
            </div>
          ) : (
            <div>
              <h3 className="card-subtitle mb-2 text-danger">Not Logged In</h3>
              <p className="card-text">Please login to access the bucket and object information.</p>
              <Link to="/login" className="btn btn-primary">
                Login
              </Link>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Home;
