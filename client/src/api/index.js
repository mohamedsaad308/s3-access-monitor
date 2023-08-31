const API_URL =
  process.env.NODE_ENV === "development" ? "http://127.0.0.1:5000" : "http://mohamedsaad308.pythonanywhere.com";

const createRequest = (access_key, secret_key) => {
  const myHeaders = new Headers();
  myHeaders.append("access-key", access_key);
  myHeaders.append("secret-key", secret_key);
  return {
    method: "GET",
    headers: myHeaders,
  };
};

export const loginUser = (cred) => {
  return fetch(`${API_URL}/api/validate-aws-credentials`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(cred),
  });
};

export const getBuckets = (access_key, secret_key) => {
  return fetch(`${API_URL}/api/buckets`, createRequest(access_key, secret_key));
};

export const getObjects = (access_key, secret_key) => {
  return fetch(`${API_URL}/api/objects`, createRequest(access_key, secret_key));
};

export const getBucketObjects = (bucketName, access_key, secret_key) => {
  return fetch(`${API_URL}/api/buckets/${bucketName}/objects`, createRequest(access_key, secret_key));
};
