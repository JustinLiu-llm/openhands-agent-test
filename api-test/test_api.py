#!/usr/bin/env python3
"""
OpenHands Agent Server API 测试脚本
Base URL: http://localhost:8000
"""

import requests
import json
import time
from typing import Optional, Dict, Any

BASE_URL = "http://localhost:8000"

class OpenHandsAPIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
        
    # ==================== Server Status ====================
    
    def get_alive(self) -> Dict[str, Any]:
        """检查服务是否存活"""
        return self.session.get(f"{self.base_url}/alive").json()
    
    def get_health(self) -> Dict[str, Any]:
        """健康检查"""
        return self.session.get(f"{self.base_url}/health").json()
    
    def get_ready(self) -> Dict[str, Any]:
        """检查服务是否就绪"""
        return self.session.get(f"{self.base_url}/ready").json()
    
    def get_server_info(self) -> Dict[str, Any]:
        """获取服务器信息"""
        return self.session.get(f"{self.base_url}/").json()
    
    # ==================== Conversations ====================
    
    def list_conversations(self, page_size: int = 50) -> Dict[str, Any]:
        """列出所有对话"""
        return self.session.get(
            f"{self.base_url}/api/conversations",
            params={"page_size": page_size, "ids": []}
        ).json()
    
    def search_conversations(self, query: str) -> Dict[str, Any]:
        """搜索对话"""
        return self.session.get(
            f"{self.base_url}/api/conversations/search",
            params={"query": query}
        ).json()
    
    def create_conversation(self, name: Optional[str] = None, 
                          llm_model: str = "openai/gemini-3-flash-preview",
                          llm_api_key: str = "sk-test",
                          llm_base_url: str = "http://localhost:8881/llm/gemini-3-flash-preview/v1") -> Dict[str, Any]:
        """创建新对话"""
        data = {
            "agent": {
                "llm": {
                    "model": llm_model,
                    "api_key": llm_api_key,
                    "base_url": llm_base_url
                },
                "tools": [
                    {"name": "terminal"},
                    {"name": "file_editor"},
                    {"name": "task_tracker"},
                    {"name": "browser_tool_set"}
                ],
                "kind": "Agent"
            },
            "workspace": {
                "working_dir": "workspace/project",
                "kind": "LocalWorkspace"
            }
        }
        if name:
            data["name"] = name
        return self.session.post(
            f"{self.base_url}/api/conversations",
            json=data
        ).json()
    
    def get_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """获取对话详情"""
        return self.session.get(
            f"{self.base_url}/api/conversations/{conversation_id}"
        ).json()
    
    def delete_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """删除对话"""
        return self.session.delete(
            f"{self.base_url}/api/conversations/{conversation_id}"
        ).json()
    
    def start_conversation(self, initial_message: str) -> Dict[str, Any]:
        """开始一个新对话并发送首条消息"""
        return self.session.post(
            f"{self.base_url}/api/conversations",
            json={"initial_message": initial_message}
        ).json()
    
    def ask_agent(self, conversation_id: str, message: str) -> Dict[str, Any]:
        """向 Agent 发送消息"""
        return self.session.post(
            f"{self.base_url}/api/conversations/{conversation_id}/ask_agent",
            json={"message": message}
        ).json()
    
    def run_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """运行对话"""
        return self.session.post(
            f"{self.base_url}/api/conversations/{conversation_id}/run"
        ).json()
    
    def pause_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """暂停对话"""
        return self.session.post(
            f"{self.base_url}/api/conversations/{conversation_id}/pause"
        ).json()
    
    # ==================== Events ====================
    
    def get_events(self, conversation_id: str, page_size: int = 50) -> Dict[str, Any]:
        """获取对话中的所有事件"""
        return self.session.get(
            f"{self.base_url}/api/conversations/{conversation_id}/events",
            params={"page_size": page_size}
        ).json()
    
    def send_message(self, conversation_id: str, message: str, msg_type: str = "text") -> Dict[str, Any]:
        """发送消息到对话"""
        return self.session.post(
            f"{self.base_url}/api/conversations/{conversation_id}/events",
            json={
                "message": message,
                "msg_type": msg_type
            }
        ).json()
    
    def search_events(self, conversation_id: str, query: str) -> Dict[str, Any]:
        """搜索对话中的事件"""
        return self.session.get(
            f"{self.base_url}/api/conversations/{conversation_id}/events/search",
            params={"query": query}
        ).json()
    
    # ==================== Bash ====================
    
    def execute_bash(self, command: str, timeout: int = 60) -> Dict[str, Any]:
        """执行 Bash 命令"""
        return self.session.post(
            f"{self.base_url}/api/bash/execute_bash_command",
            json={
                "command": command,
                "timeout": timeout
            }
        ).json()
    
    def start_bash(self, command: str) -> Dict[str, Any]:
        """开始一个 Bash 命令（异步）"""
        return self.session.post(
            f"{self.base_url}/api/bash/start_bash_command",
            json={"command": command}
        ).json()
    
    # ==================== Files ====================
    
    def upload_file(self, file_path: str, remote_path: str) -> Dict[str, Any]:
        """上传文件"""
        with open(file_path, 'rb') as f:
            files = {'file': f}
            return self.session.post(
                f"{self.base_url}/api/file/upload/{remote_path}",
                files=files
            ).json()
    
    def download_file(self, remote_path: str) -> bytes:
        """下载文件"""
        return self.session.get(
            f"{self.base_url}/api/file/download/{remote_path}"
        ).content
    
    # ==================== Tools ====================
    
    def list_tools(self) -> Dict[str, Any]:
        """列出可用工具"""
        return self.session.get(f"{self.base_url}/api/tools/").json()
    
    # ==================== LLM ====================
    
    def list_llm_providers(self) -> Dict[str, Any]:
        """列出 LLM 提供商"""
        return self.session.get(f"{self.base_url}/api/llm/providers").json()
    
    def list_llm_models(self) -> Dict[str, Any]:
        """列出可用模型"""
        return self.session.get(f"{self.base_url}/api/llm/models").json()


# ==================== 测试用例 ====================

def test_server_status():
    """测试服务器状态"""
    client = OpenHandsAPIClient()
    
    print("=" * 50)
    print("测试服务器状态")
    print("=" * 50)
    
    alive = client.get_alive()
    print(f"Alive: {alive}")
    
    health = client.get_health()
    print(f"Health: {health}")
    
    ready = client.get_ready()
    print(f"Ready: {ready}")
    
    info = client.get_server_info()
    print(f"Server Info: {info}")
    print()


def test_conversations():
    """测试对话功能"""
    client = OpenHandsAPIClient()
    
    print("=" * 50)
    print("测试对话功能")
    print("=" * 50)
    
    # 创建对话
    conv = client.create_conversation(name="测试对话")
    print(f"创建对话: {conv}")
    
    if "conversation_id" in conv:
        conv_id = conv["conversation_id"]
        
        # 发送消息
        msg = client.send_message(conv_id, "你好！")
        print(f"发送消息: {msg}")
        
        # 获取对话事件
        events = client.get_events(conv_id)
        print(f"对话事件: {events}")
        
        # 询问 Agent
        response = client.ask_agent(conv_id, "帮我执行一个 ls 命令")
        print(f"Agent 响应: {response}")
        
        # 删除对话
        delete_result = client.delete_conversation(conv_id)
        print(f"删除对话: {delete_result}")
    
    # 列出所有对话
    convs = client.list_conversations()
    print(f"对话列表: {convs}")
    print()


def test_bash_command():
    """测试 Bash 命令执行"""
    client = OpenHandsAPIClient()
    
    print("=" * 50)
    print("测试 Bash 命令")
    print("=" * 50)
    
    result = client.execute_bash("echo 'Hello from OpenHands' && date")
    print(f"Bash 执行结果: {result}")
    print()


def test_tools_and_llm():
    """测试工具和 LLM"""
    client = OpenHandsAPIClient()
    
    print("=" * 50)
    print("测试工具和 LLM")
    print("=" * 50)
    
    tools = client.list_tools()
    print(f"可用工具: {tools}")
    
    providers = client.list_llm_providers()
    print(f"LLM 提供商: {providers}")
    
    models = client.list_llm_models()
    print(f"可用模型: {models}")
    print()


def interactive_chat():
    """交互式聊天"""
    client = OpenHandsAPIClient()
    
    print("=" * 50)
    print("交互式聊天")
    print("=" * 50)
    print("输入 'quit' 退出")
    print()
    
    # 创建新对话
    conv = client.create_conversation()
    if "conversation_id" not in conv:
        print("创建对话失败!")
        return
    
    conv_id = conv["conversation_id"]
    print(f"对话 ID: {conv_id}")
    print()
    
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        
        if not user_input.strip():
            continue
        
        print("Agent: ", end="", flush=True)
        
        # 发送消息并获取响应
        response = client.ask_agent(conv_id, user_input)
        print(json.dumps(response, indent=2, ensure_ascii=False))
        print()


def chat_with_streaming(conversation_id: str, message: str):
    """带流式输出的聊天（如果支持）"""
    client = OpenHandsAPIClient()
    
    # 发送消息
    response = client.ask_agent(conversation_id, message)
    return response


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "status":
            test_server_status()
        elif command == "conversations":
            test_conversations()
        elif command == "bash":
            test_bash_command()
        elif command == "tools":
            test_tools_and_llm()
        elif command == "chat":
            interactive_chat()
        elif command == "all":
            test_server_status()
            test_conversations()
            test_bash_command()
            test_tools_and_llm()
        else:
            print(f"未知命令: {command}")
            print("可用命令: status, conversations, bash, tools, chat, all")
    else:
        # 默认运行所有测试
        test_server_status()
        test_conversations()
        test_bash_command()
        test_tools_and_llm()
