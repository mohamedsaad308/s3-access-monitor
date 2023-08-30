import React from "react";

function ListBuckets({ buckets, permissionStatus }) {
  return (
    <div>
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>Bucket Name</th>
            <th>Owner</th>
            <th>Permission</th>
            <th>Creation Date</th>
          </tr>
        </thead>
        <tbody>
          {buckets.map((bucket, index) => (
            <tr key={index}>
              <td>{bucket.bucket_name}</td>
              <td>{bucket.bucket_owner}</td>
              <td>{permissionStatus}</td>
              <td>{bucket.creation_date}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ListBuckets;
