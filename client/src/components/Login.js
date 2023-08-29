import React, { useState } from "react";
import { loginUser } from "../api";
import { useNavigate } from "react-router";
function Login() {
  const navigate = useNavigate();
  const [accessKeyId, setAccessKeyId] = useState("");
  const [secretAccessKey, setSecretAccessKey] = useState("");
  const [error, setError] = useState(null);
  const handleAccessKeyIdChange = (event) => {
    setAccessKeyId(event.target.value);
  };

  const handleSecretAccessKeyChange = (event) => {
    setSecretAccessKey(event.target.value);
  };

  const handleLogin = () => {
    loginUser({ access_key: accessKeyId, secret_key: secretAccessKey })
      .then((response) => response.json())
      .then((result) => {
        if (result.valid) {
          localStorage.setItem("accessKeyId", accessKeyId);
          localStorage.setItem("secretAccessKey", secretAccessKey);
          navigate("/");
        } else {
          setError("Your AWS credentials are not valid!");
        }
      })
      .catch((error) => {
        console.log("error", error);
      });
  };

  return (
    <div className="d-flex justify-content-center align-items-center min-vh-100">
      <div className="card w-50">
        <div className="card-body">
          <h2 className="card-title">Login</h2>
          {error && <p className="text-danger">{error}</p>}
          <div className="form-group">
            <label>Access Key ID:</label>
            <input
              type="text"
              value={accessKeyId}
              onChange={handleAccessKeyIdChange}
              className="form-control"
              placeholder="Enter Access Key ID"
            />
          </div>
          <div className="form-group">
            <label>Secret Access Key:</label>
            <input
              type="password"
              value={secretAccessKey}
              onChange={handleSecretAccessKeyChange}
              className="form-control"
              placeholder="Enter Secret Access Key"
            />
          </div>
          <button onClick={handleLogin} className="btn btn-primary">
            Login
          </button>
        </div>
      </div>
    </div>
  );
}

export default Login;
