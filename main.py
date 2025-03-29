# main.py
# 主应用入口

from fastapi import FastAPI
from routes import router

# 创建FastAPI应用
app = FastAPI()

# 注册路由
app.include_router(router)

# 添加健康检查路由
@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)