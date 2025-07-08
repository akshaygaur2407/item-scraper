import { useEffect, useRef, useState } from "react";

const ResultCard = ({ query, country, results, onBack, loading }) => {
  const tableContainerRef = useRef(null);
  const [showScrollHint, setShowScrollHint] = useState(false);

  const checkOverflow = () => {
    const el = tableContainerRef.current;
    if (!el) return;
    setShowScrollHint(el.scrollHeight > el.clientHeight);
  };

  useEffect(() => {
    checkOverflow();
  }, [results]);

  useEffect(() => {
    const el = tableContainerRef.current;
    if (!el) return;

    const onScroll = () => {
      const atBottom = el.scrollTop + el.clientHeight >= el.scrollHeight;
      setShowScrollHint(!atBottom);
    };

    el.addEventListener("scroll", onScroll);
    window.addEventListener("resize", checkOverflow);

    return () => {
      el.removeEventListener("scroll", onScroll);
      window.removeEventListener("resize", checkOverflow);
    };
  }, []);

  return (
    <div
      className="card p-4 w-100 position-relative"
      style={{ maxWidth: "800px", minHeight: "300px", minWidth: "320px" }}
    >
      <div className="d-flex justify-content-between align-items-center mb-3">
        <button className="btn btn-sm btn-secondary" onClick={onBack}>
          ← Back
        </button>
        <h5 className="mb-0">
          Results for "{query}" ({country})
        </h5>
      </div>

      {loading ? (
        <div
          className="d-flex justify-content-center align-items-center"
          style={{ height: "200px" }}
        >
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      ) : results.length === 0 ? (
        <div>No results found.</div>
      ) : (
        <>
          {/* Scrollable Table */}
          <div
            ref={tableContainerRef}
            style={{
              maxHeight: "420px",
              overflowY: "auto",
            }}
          >
            <table className="table table-bordered table-hover mb-0">
              <thead
                className="table-light"
                style={{ position: "sticky", top: 0, zIndex: 1 }}
              >
                <tr>
                  <th style={{ width: "10%" }}>Thumbnail</th>
                  <th style={{ width: "25%" }}>Product</th>
                  <th style={{ width: "10%" }}>Price</th>
                  <th style={{ width: "10%" }}>Currency</th>
                  <th style={{ width: "20%" }}>Seller</th>
                  <th style={{ width: "25%" }}>Link</th>
                </tr>
              </thead>
              <tbody>
                {results.map((item, idx) => (
                  <tr key={idx}>
                    <td>
                      {item.thumbnail ? (
                        <img
                          src={item.thumbnail}
                          alt="Thumbnail"
                          style={{ width: "50px", height: "auto" }}
                        />
                      ) : (
                        "N/A"
                      )}
                    </td>
                    <td style={{ wordBreak: "break-word" }}>{item.productName}</td>
                    <td>{item.price}</td>
                    <td>{item.currency}</td>
                    <td>{item.seller || "N/A"}</td>
                    <td style={{ wordBreak: "break-word" }}>
                      <a
                        href={item.link}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ wordBreak: "break-all" }}
                      >
                        {item.link}
                      </a>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          {/* Scroll Hint */}
          {showScrollHint && (
            <div
              className="position-absolute w-100 text-center"
              style={{
                bottom: 0,
                left: 0,
                height: "40px",
                background: "linear-gradient(to top, #fff, transparent)",
                pointerEvents: "none",
                display: "flex",
                justifyContent: "center",
                alignItems: "flex-end",
              }}
            >
              <span style={{ fontSize: "1.4rem", opacity: 0.6 }}>↓</span>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default ResultCard;