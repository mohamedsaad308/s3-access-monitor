import React from "react";
import { Link } from "react-router-dom";

function ListObjects({ objects }) {
  if (!objects.length) return <p>Yoh have no objects under this section!</p>;
  return (
    <div>
      <table className="table table-bordered">
        <thead>
          <tr>
            <th>File Name</th>
            <th>Bucket</th>
            <th>URL</th>
          </tr>
        </thead>
        <tbody>
          {objects.map((object, index) => (
            <tr key={index}>
              <td>{object.key}</td>
              <td>
                <Link to={`/buckets/${object.bucket}/objects`}>{object.bucket}</Link>
              </td>
              <td>
                {" "}
                <Link target="_blank" to={object.url}>
                  {object.url}
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default ListObjects;
