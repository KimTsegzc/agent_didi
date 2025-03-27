# server.py
from mcp.server.fastmcp import FastMCP
from L0_OpenAI import L0_OpenAI_VL, L0_OpenAI_TTS, L0_OpenAI_chat
import Agent_didi_v1_L2 as didi
from playsound import playsound

# Create an MCP server
mcp = FastMCP("Didi_agent")

# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!\n"

# Add an addition tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    response = get_greeting("Alice")
    return response + str(a + b)

@mcp.tool()
def didi_agent(human_input: str) -> str:
    try:
        """Call the didi agent"""
        prompt = '这是一句用户从出发地到目的地的描述，请提取出出发地和目的地'
        prompt += '注意严格按照出发地=，目的地='
        prompt += '单行单句，不要有问候性回答，用户的描述是：'
        prompt += human_input
        response = L0_OpenAI_chat(prompt)
        from_pos = response.split('=')[1].split('，')[0]
        to_pos = response.split('=')[2].split('，')[0]
        return didi_call_service(from_pos, to_pos)
    except Exception as e:
        return str(e)


@mcp.tool()
def didi_call_service(from_pos: str, to_pos: str) -> str:
    try:
        didi.call_service(from_pos, to_pos)
        prompt = '这是一个打车软件，用户刚完成订单输入'
        prompt += '请先用一句话介绍目前选中服务，应答时间、价格、里程、行程时间'
        prompt += '然后依次介绍各类服务价格'
        prompt += '注意，各类价格精确到元即可，不用小数点后面的内容'
        prompt += '不要开头和结尾的问候性回答，精简一点'
        url = "./snapshot.png"
        posi = didi.switch_to_app_and_snapshot("滴滴")
        response = L0_OpenAI_VL(prompt, url).replace('*', '')
        L0_OpenAI_TTS(response)
        playsound('./media/output.mp3')
        return response
    except Exception as e:
        return str(e)
