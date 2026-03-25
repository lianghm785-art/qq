import requests
import os
import sys

# ========== 从环境变量读取配置 ==========
YOUR_QQ = os.environ.get("YOUR_QQ")
API_KEY = os.environ.get("DOUBAO_API_KEY")
QMSG_KEY = os.environ.get("QMSG_KEY")
# ===================================

def get_ai_remind():
    """调用豆包 API 生成睡前提醒"""
    url = "https://api.doubao.com/v1/chat/completions"
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": "doubao-pro",  # 可选 doubao-pro 或 doubao-lite
        "messages": [
            {"role": "system", "content": "你是一个温柔贴心的晚安助手，说话简短温暖。"},
            {"role": "user", "content": "用温柔简短的语气提醒我该睡觉了，关心一点，15字左右"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        result = response.json()
        # 解析返回结果
        content = result["choices"][0]["message"]["content"]
        print(f"AI 生成内容: {content}")
        return content
    except Exception as e:
        print(f"API 调用失败: {e}")
        return "早点休息哦，晚安~"  # 降级文案

def send_to_qq(qq, content):
    """通过 Qmsg 酱发送 QQ 消息"""
    if not QMSG_KEY:
        print("错误: QMSG_KEY 未配置")
        return False
    
    url = f"https://qmsg.zendee.cn/send/{QMSG_KEY}/{qq}"
    try:
        response = requests.get(url, params={"msg": f"💤 睡觉提醒\n{content}"}, timeout=10)
        print(f"发送结果: {response.text}")
        return True
    except Exception as e:
        print(f"发送失败: {e}")
        return False

if __name__ == "__main__":
    # 检查必要配置
    if not YOUR_QQ:
        print("错误: YOUR_QQ 未配置")
        sys.exit(1)
    if not API_KEY:
        print("错误: DOUBAO_API_KEY 未配置")
        sys.exit(1)
    
    remind_text = get_ai_remind()
    send_to_qq(YOUR_QQ, remind_text)
    print("提醒任务执行完成")
