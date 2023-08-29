export const loginUser = (user) => {
  return fetch("http://127.0.0.1:5000/api/validate-aws-credentials", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(user),
  });
};
