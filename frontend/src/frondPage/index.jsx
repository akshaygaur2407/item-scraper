import { useState } from "react";
import axios from "axios";
import ResultCard from "./ResultCard";

const MainComponent = () => {
  const [query, setQuery] = useState("");
  const [submittedQuery, setSubmittedQuery] = useState("");
  const [submittedCountry, setSubmittedCountry] = useState("");
  const [country, setCountry] = useState("US");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [searched, setSearched] = useState(false); // <— new flag

  const handleSearch = async () => {
    if (!query.trim()) return;
  
    setLoading(true);
    setError("");
    setResults([]);
  
    try {
      const { data } = await axios.get("https://item-scraper-backend.onrender.com/search", {
        params: {
          query,
          country,
        },
      });
      setResults(data);
      setSubmittedQuery(query);
      setSubmittedCountry(country);
      setSearched(true);
    } catch (err) {
      console.error(err);
      setError("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };
  

  return (
    <div
      className="container-fluid d-flex justify-content-center align-items-start"
      style={{
        minHeight: "100vh",
        background: "transparent",
        padding: "40px 20px",
      }}
    >
      <div
        className="d-flex flex-column flex-md-row gap-4 w-100"
        style={{ maxWidth: "1200px" }}
      >
        {/* ─── Search Card ─────────────────────────────────────── */}
        <div
          className="card p-4 w-100" // 👈 shadow removed
          style={{
            width: "100%",
            maxWidth: "620px",
            minWidth:"300px",
            minHeight: "450px",
            borderRadius: "16px",
            backgroundColor: "#ffffff",
          }}
        >
          <h4 className="mb-4 text-center text-primary fw-semibold">
            Search Product
          </h4>

          <div className="mb-3">
            <label className="form-label fw-semibold">Product Query</label>
            <input
              type="text"
              className="form-control"
              placeholder="e.g. iPhone 16 Pro, 128GB"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
            />
          </div>

          <div className="mb-3">
            <label className="form-label fw-semibold">Country</label>
            <select
              className="form-select"
              value={country}
              onChange={(e) => setCountry(e.target.value)}
            >
              <option value="US">United States</option>
              <option value="IN">India</option>
              <option value="UK">United Kingdom</option>
              <option value="CA">Canada</option>
              <option value="AU">Australia</option>
            </select>
          </div>

          <button
            className="btn btn-primary w-100 fw-medium"
            onClick={handleSearch}
            disabled={loading}
            style={{ marginTop: "20px" }}
          >
            {loading ? "Searching..." : "Search"}
          </button>

          {error && (
            <div
              className="alert alert-danger mt-3 text-center"
              style={{ fontSize: "0.95rem" }}
            >
              {error}
            </div>
          )}
        </div>

        {searched && (
          <ResultCard
            query={submittedQuery}
            country={submittedCountry}
            results={results}
            onBack={() => setSearched(false)}
            loading={loading}
          />
        )}
      </div>
    </div>
  );
};

export default MainComponent;
