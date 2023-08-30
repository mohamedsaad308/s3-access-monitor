// src/App.js
import { Route, Routes } from "react-router-dom";
import React from "react";
import "./App.css";
import Layout from "./components/layout/Layout";
import Home from "./components/Home";
import Login from "./components/Login";
import ListBucketsPage from "./pages/AllBucketsPage";
import ListObjectsPage from "./pages/AllObjectsPage";

function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Home />} exact />
        <Route path="/login" element={<Login />} exact />
        <Route path="/buckets" element={<ListBucketsPage />} exact />
        <Route path="/objects" element={<ListObjectsPage />} exact />
      </Routes>
    </Layout>
  );
}

export default App;
