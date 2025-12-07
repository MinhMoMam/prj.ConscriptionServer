import myPackages.server as sv
import uvicorn

if __name__ == "__main__":
    uvicorn.run(sv.app, host="127.0.0.1", port=8000)