import httpx

def async_client() -> httpx.AsyncClient:
    return httpx.AsyncClient(timeout=10)
