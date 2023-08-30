import React, { useState, useEffect } from "react";
import ListObjects from "../components/ListObjects";
import { getBucketObjects } from "../api";
import Loading from "../components/layout/Loading";
import { useParams } from "react-router-dom";

function BucketObjectsPage() {
  const [allObjects, setAllObjects] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [showPublic, setShowPublic] = useState(true);
  const [showPrivate, setShowPrivate] = useState(true);
  const { bucketName } = useParams();

  useEffect(() => {
    getBucketObjects(bucketName, localStorage.getItem("accessKeyId"), localStorage.getItem("secretAccessKey"))
      .then((res) => res.json())
      .then((result) => {
        setAllObjects(result);
        setIsLoading(false);
      })
      .catch((error) => console.log(error));
  }, [bucketName]);
  if (isLoading) {
    return <Loading />;
  }
  return (
    <div>
      <h2>Objects Statistics</h2>
      <p>
        {bucketName} has {allObjects["private_objects_count"]} private files, and {allObjects["public_objects_count"]}{" "}
        public files.
      </p>
      <button onClick={() => setShowPublic(!showPublic)} className="mr-2">
        {showPublic ? "Hide Public Buckets" : "Show Public Buckets"}
      </button>
      <button onClick={() => setShowPrivate(!showPrivate)}>
        {showPrivate ? "Hide Private Buckets" : "Show Private Buckets"}
      </button>
      {showPublic && (
        <div className="mt-2">
          <h2>Public Objects</h2>
          <ListObjects objects={allObjects["public_objects"]} permissionStatus="Public" />
        </div>
      )}
      {showPrivate && (
        <div>
          <h2>Private Objects</h2>
          <ListObjects objects={allObjects["private_objects"]} permissionStatus="Private" />
        </div>
      )}
    </div>
  );
}

export default BucketObjectsPage;
