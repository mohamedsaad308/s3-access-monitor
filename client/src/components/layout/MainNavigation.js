import React from "react";
import { Link } from "react-router-dom";
import { useNavigate } from "react-router";
function MainNavigation() {
  const navigate = useNavigate();
  const logoutHandler = (event) => {
    event.preventDefault();
    localStorage.removeItem("secretAccessKey");
    localStorage.removeItem("accessKeyId");
    navigate("/login");
  };
  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <Link className="navbar-brand " to="/">
        S3 Dashboard
      </Link>
      <div className="collapse navbar-collapse">
        <ul className="navbar-nav mr-auto">
          {localStorage.getItem("secretAccessKey") ? (
            <li className="nav-item ">
              <Link className="nav-link" to="#" onClick={logoutHandler}>
                Logout
              </Link>
            </li>
          ) : (
            ""
          )}
          {localStorage.getItem("secretAccessKey") ? (
            <li className="nav-item ">
              <Link className="nav-link" to="/buckets">
                Buckets
              </Link>
            </li>
          ) : (
            ""
          )}
          {localStorage.getItem("secretAccessKey") ? (
            <li className="nav-item ">
              <Link className="nav-link" to="/objects">
                Objects
              </Link>
            </li>
          ) : (
            ""
          )}
          {!localStorage.getItem("secretAccessKey") ? (
            <li className="nav-item ">
              <Link className="nav-link" to="/login">
                Login
              </Link>
            </li>
          ) : (
            ""
          )}
        </ul>
      </div>
    </nav>
  );
}

export default MainNavigation;
