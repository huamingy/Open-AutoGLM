from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import subprocess
import sys
import os
import asyncio
import uvicorn

DEVICE_ID = "192.168.2.233:5555"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4"
MODEL = "autoglm-phone"
API_KEY = "56879d68a6924df8b00565b78118940b.sGc713q5SfN8WbzN"

app = FastAPI()

# Global agent instance for termination
current_agent = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/terminate")
async def terminate_task():
    """Terminate the currently running task."""
    if current_agent and not current_agent.is_terminated():
        current_agent.terminate()
        return {"status": "success", "message": "Task terminated"}
    return {"status": "error", "message": "No active task to terminate"}

@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()

    # 安全的WebSocket发送函数
    async def safe_send_text(text: str):
        try:
            await websocket.send_text(text)
        except Exception:
            # 连接已断开，忽略错误
            pass

    try:
        while True:
            try:
                data = await websocket.receive_json()
            except Exception as e:
                # WebSocket连接断开或其他接收错误
                print(f"WebSocket接收错误: {e}")
                break

            # 检查是否是终止命令
            if data.get("action") == "terminate":
                if current_agent and not current_agent.is_terminated():
                    current_agent.terminate()
                    await safe_send_text("✅ 任务已终止\n")
                else:
                    await safe_send_text("⚠️ 没有正在运行的任务\n")
                continue

            # 检查是否是心跳包
            if data.get("type") == "ping":
                pong_response = {"type": "pong", "timestamp": data.get("timestamp")}
                try:
                    await websocket.send_json(pong_response)
                except Exception:
                    # 连接已断开，忽略错误
                    pass
                continue

            # 处理普通文本命令
            text = data.get("text", "").strip()
            if not text:
                await safe_send_text("❌ empty command")
                continue

            await safe_send_text(f"开始执行：{text}\n")

            # Create agent instance for this task
            from phone_agent import PhoneAgent
            from phone_agent.agent import AgentConfig
            from phone_agent.model import ModelConfig
            import io
            import sys
            import contextlib

            model_config = ModelConfig(
                base_url=BASE_URL,
                model_name=MODEL,
                api_key=API_KEY,
            )

            agent_config = AgentConfig(
                device_id=DEVICE_ID,
                verbose=True,
                enable_visual_feedback=True,  # Enable visual feedback
            )

            current_agent = PhoneAgent(
                model_config=model_config,
                agent_config=agent_config,
                websocket=websocket,  # Pass websocket for real-time screen status updates
            )

            # Prepare screen in async context before starting the sync thread
            await websocket.send_text("检查并准备屏幕...\n")
            from phone_agent.adb import prepare_screen_for_operation
            screen_ready = prepare_screen_for_operation(DEVICE_ID)
            if screen_ready:
                await websocket.send_text("屏幕已准备就绪\n")
            else:
                await websocket.send_text("屏幕准备失败，操作可能受影响\n")

            # Create a queue for output messages
            import queue
            output_queue = queue.Queue()

            # Create a custom output stream to capture prints
            class WebSocketOutput:
                def __init__(self):
                    self.buffer = ""

                def write(self, text):
                    if text:
                        self.buffer += text
                        # Send complete lines to queue
                        while '\n' in self.buffer:
                            line, self.buffer = self.buffer.split('\n', 1)
                            if line.strip():  # Only send non-empty lines
                                output_queue.put(line + '\n')

                def flush(self):
                    if self.buffer:
                        output_queue.put(self.buffer)
                        self.buffer = ""

                def isatty(self):
                    return False

            # Capture stdout and redirect to WebSocket
            ws_output = WebSocketOutput()
            old_stdout = sys.stdout

            try:
                # Redirect stdout to our output capturer
                sys.stdout = ws_output

                # Run task in background thread
                import threading
                result = None
                task_error = None

                def run_task():
                    nonlocal result, task_error
                    try:
                        result = current_agent.run(text)
                    except Exception as e:
                        task_error = str(e)

                task_thread = threading.Thread(target=run_task, daemon=True)
                task_thread.start()

                # Monitor output queue and send to WebSocket
                while task_thread.is_alive() or not output_queue.empty():
                    try:
                        # Send available output
                        while not output_queue.empty():
                            message = output_queue.get_nowait()
                            await safe_send_text(message)

                        # Check if task is terminated
                        if current_agent.is_terminated():
                            await safe_send_text("\n❌ 任务已被终止\n")
                            break

                        await asyncio.sleep(0.05)  # Small delay to avoid busy waiting

                    except queue.Empty:
                        await asyncio.sleep(0.05)

                # Send remaining output
                while not output_queue.empty():
                    message = output_queue.get_nowait()
                    await safe_send_text(message)

                # Flush any remaining buffer
                ws_output.flush()
                while not output_queue.empty():
                    message = output_queue.get_nowait()
                    await safe_send_text(message)

                # Send final result
                if task_error:
                    await safe_send_text(f"\n❌ 执行出错: {task_error}\n")
                elif not current_agent.is_terminated() and result is not None:
                    await safe_send_text(f"\nResult: {result}\n")

            except Exception as e:
                await safe_send_text(f"\n❌ WebSocket错误: {e}\n")
                print(f"WebSocket错误: {e}")
            finally:
                # Restore stdout
                sys.stdout = old_stdout
                # Reset agent
                current_agent = None

    except WebSocketDisconnect:
        print("WebSocket disconnected")


if __name__ == "__main__":
    # 设置控制台编码为UTF-8
    import os
    if os.name == 'nt':  # Windows
        os.system('chcp 65001 >nul 2>&1')

    print("启动 AutoGLM WebSocket 服务器...")
    print("设备 ID:", DEVICE_ID)
    print("模型 URL:", BASE_URL)
    print("模型名称:", MODEL)
    print("WebSocket 地址: ws://localhost:8002/ws")
    print("HTTP 地址: http://localhost:8002")
    print("\n在浏览器中打开 index.html 开始使用\n")

    uvicorn.run(
        app,
        host="0.0.0.0",  # 允许外部访问
        port=8002,
        log_level="info"
    )
