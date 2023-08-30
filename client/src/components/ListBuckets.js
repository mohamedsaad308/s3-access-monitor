import React from "react";
import { Link } from "react-router-dom";
function ListBuckets({ buckets, permissionStatus }) {
  if (!buckets.length) return <p>Yoh have no buckets under this section!</p>;
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
              <td>
                {" "}
                <Link to={`/buckets/${bucket.bucket_name}/objects`}>{bucket.bucket_name}</Link>
              </td>
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
