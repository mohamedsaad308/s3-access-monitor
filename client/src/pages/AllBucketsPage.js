import React, { useState, useEffect } from "react";
import ListBuckets from "../components/ListBuckets";
import { getBuckets } from "../api";
import Loading from "../components/layout/Loading";
function ListBucketsPage() {
  const [allBuckets, setAllBuckets] = useState({});
  const [isLoading, setIsLoading] = useState(true);
  const [showPublic, setShowPublic] = useState(true);
  const [showPrivate, setShowPrivate] = useState(true);

  useEffect(() => {
    getBuckets(localStorage.getItem("accessKeyId"), localStorage.getItem("secretAccessKey"))
      .then((res) => res.json())
      .then((result) => {
        setAllBuckets(result);
        setIsLoading(false);
      })
      .catch((error) => console.log(error));
  }, []);
  if (isLoading) {
    return <Loading />;
  }
  return (
    <div>
      <h2>Bucket Statistics</h2>
      <p>
        You have {allBuckets["private_buckets_count"]} private bucket, and {allBuckets["public_buckets_count"]}.
      </p>
      <button onClick={() => setShowPublic(!showPublic)} className="mr-2">
        {showPublic ? "Hide Public Buckets" : "Show Public Buckets"}
      </button>
      <button onClick={() => setShowPrivate(!showPrivate)}>
        {showPrivate ? "Hide Private Buckets" : "Show Private Buckets"}
      </button>
      {showPublic && (
        <div className="mt-2">
          <h2>Public Buckets</h2>
          <ListBuckets buckets={allBuckets["public_buckets"]} permissionStatus="Bucket and Objects can be public" />
        </div>
      )}
      {showPrivate && (
        <div>
          <h2>Private Buckets</h2>
          <ListBuckets buckets={allBuckets["private_buckets"]} permissionStatus="Private" />
        </div>
      )}
    </div>
  );
}

export default ListBucketsPage;
