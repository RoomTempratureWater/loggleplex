import uvicorn

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server.api:app", host="0.0.0.0", port=3000, reload=True)