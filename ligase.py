import streamlit as st

st.set_page_config(layout="wide", page_title="DNA连接酶模拟器")
st.title("🧬 基因工程：黏性末端与平末端的拼接")

# 顶部切换菜单
mode = st.radio("请选择末端类型：", ["黏性末端 (Sticky Ends)", "平末端 (Blunt Ends)"], horizontal=True)

# 状态管理 (切换模式时自动重置)
if 'step' not in st.session_state or 'mode' not in st.session_state or st.session_state.mode != mode:
    st.session_state.step = 0 # 0: 分离, 1: 靠近咬合, 2: 缝合
    st.session_state.mode = mode

st.markdown("---")

# ================= 重点：平末端缺点警示框 =================
if mode == "平末端 (Blunt Ends)":
    st.error("""
    🚨 **平末端的致命缺点**：
    1. **连接效率极低**：没有互补单链的氢键辅助，只能靠 DNA 连接酶强行“硬拼”。
    2. **方向不可控**：缺乏定向识别信号，容易发生**反向连接**或**自身环化**。
    """)
else:
    st.success("""
    ✅ **黏性末端的优势**：
    1. **连接效率高**：突出的单链能通过氢键自动精准配对（榫卯结构）。
    2. **定向插入**：两端切口不同，保证目的基因正向插入载体，不会接反。
    """)

st.markdown("---")

st.markdown("""
<style>
    /* 焊接金光特效 */
    @keyframes weld {
        0% { box-shadow: inset 0 0 0px #ffeb3b, 0 0 0px #ffeb3b; }
        50% { box-shadow: inset 0 0 20px #ffeb3b, 0 0 15px #ffeb3b; }
        100% { box-shadow: inset 0 0 0px #ffeb3b, 0 0 0px #ffeb3b; }
    }

    .canvas { background-color: #ffffff; border: 2px solid #e0e0e0; border-radius: 8px; padding: 100px 50px; display: flex; justify-content: center; position: relative; overflow: hidden; }
    
    /* 整个动画容器 */
    .dna-scene { position: relative; width: 800px; height: 100px; }
    
    /* 左边载体 */
    .left-part { position: absolute; left: 50px; top: 0; }
    
    /* 右边基因 */
    .right-part { position: absolute; left: 210px; top: 0; transition: transform 1s ease-in-out; }
    
    /* 距离控制 */
    .shift-away { transform: translateX(400px); } 
    .shift-close { transform: translateX(0px); }  

    /* 核心方块 */
    .row { display: flex; height: 40px; }
    .block { 
        width: 40px; height: 40px; 
        display: flex; justify-content: center; align-items: center;
        font-family: monospace; font-size: 18px; font-weight: bold;
        border: 1px solid rgba(0,0,0,0.15); margin: 0; padding: 0;
        box-sizing: border-box;
    }
    
    /* 颜色 */
    .c-left { background-color: #37474f; color: white; }
    .c-right { background-color: #d32f2f; color: white; }
    
    /* 缺口的空位（透明） */
    .c-empty { visibility: hidden; border: none; }
    
    /* 缝合时，两对结合碱基的金光特效 */
    .sealed-base { animation: weld 1.2s infinite; border: 2px solid #ffeb3b !important; z-index: 10; }
    
    /* 连接酶火花位置 */
    .spark { position: absolute; font-size: 28px; z-index: 20; animation: pop 0.5s ease-out; }
    
    @keyframes pop {
        0% { transform: scale(0); opacity: 0; }
        100% { transform: scale(1); opacity: 1; }
    }
</style>
""", unsafe_allow_html=True)

def render_blocks(seq, css_class, is_sealed=False):
    if not is_sealed:
        return "".join([f"<div class='block {css_class}'>{c}</div>" for c in seq])
    else:
        return "".join([f"<div class='block {css_class} sealed-base'>{c}</div>" for c in seq])

def render_empty(count):
    return "<div class='block c-empty'>X</div>" * count

is_sealed = True if st.session_state.step == 2 else False
shift_class = "shift-close" if st.session_state.step >= 1 else "shift-away"

html = "<div class='canvas'><div class='dna-scene'>"

# ================= 内容渲染 =================

if mode == "黏性末端 (Sticky Ends)":
    # 左侧：切开的载体
    html += "<div class='left-part'>"
    html += "<div class='row'>" + render_blocks("ATCG", "c-left") + render_blocks("AATT", "c-left", is_sealed) + "</div>"
    html += "<div class='row'>" + render_blocks("TAGC", "c-left") + render_empty(4) + "</div>"
    html += "</div>"

    # 右侧：目的基因
    html += f"<div class='right-part {shift_class}'>"
    html += "<div class='row'>" + render_empty(4) + render_blocks("GC", "c-right") + "<div style='font-size: 24px; font-weight: bold; padding: 0 10px; display: flex; align-items: center; letter-spacing: 2px;'>......</div></div>"
    html += "<div class='row'>" + render_blocks("TTAA", "c-right", is_sealed) + render_blocks("CG", "c-right") + "<div style='font-size: 24px; font-weight: bold; padding: 0 10px; display: flex; align-items: center; letter-spacing: 2px;'>......</div></div>"
    html += "</div>"
    
    # 黏性末端的火花位置（错开的接缝）
    if st.session_state.step == 2:
        html += f"<div class='spark' style='left: 202px; top: 0px;'>✨</div>"
        html += f"<div class='spark' style='left: 202px; top: 40px;'>✨</div>"

else:
    # 左侧：平齐的载体
    html += "<div class='left-part'>"
    html += "<div class='row'>" + render_blocks("ATCG", "c-left", is_sealed) + "</div>"
    html += "<div class='row'>" + render_blocks("TAGC", "c-left", is_sealed) + "</div>"
    html += "</div>"

    # 右侧：平齐的基因
    html += f"<div class='right-part {shift_class}'>"
    html += "<div class='row'>" + render_blocks("AATT", "c-right", is_sealed) + "<div style='font-size: 24px; font-weight: bold; padding: 0 10px; display: flex; align-items: center; letter-spacing: 2px;'>......</div></div>"
    html += "<div class='row'>" + render_blocks("TTAA", "c-right", is_sealed) + "<div style='font-size: 24px; font-weight: bold; padding: 0 10px; display: flex; align-items: center; letter-spacing: 2px;'>......</div></div>"
    html += "</div>"
    
    # 平末端的火花位置（同一垂直线的上下两处）
    if st.session_state.step == 2:
        html += f"<div class='spark' style='left: 202px; top: 0px;'>✨</div>"
        html += f"<div class='spark' style='left: 202px; top: 40px;'>✨</div>"

html += "</div></div>"
st.markdown(html, unsafe_allow_html=True)

# ================= 操作按钮 =================
st.markdown("<br><br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔄 重置"):
        st.session_state.step = 0
        st.rerun()

with col2:
    if st.button("➡️ 1. 靠近（自动寻找接合点）"):
        st.session_state.step = 1
        st.rerun()

with col3:
    if st.button("✨ 2. DNA连接酶缝合骨架"):
        st.session_state.step = 2
        st.rerun()

# 水印
st.markdown(
    """
    <div style="position: fixed; bottom: 40px; left: 50%; transform: translateX(-50%); opacity: 0.3; z-index: 9999; font-size: 14px; color: gray; pointer-events: none; letter-spacing: 2px;">
        © 诸葛先生
    </div>
    """,
    unsafe_allow_html=True
)
