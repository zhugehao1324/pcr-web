import streamlit as st

st.set_page_config(layout="wide", page_title="PCR 模拟器")
st.title("🧪 PCR 试管环境：引物延伸与半保留复制模拟器")

# 1. 初始化状态
if 'cycle' not in st.session_state:
    st.session_state.cycle = 0
if 'phase' not in st.session_state:
    st.session_state.phase = "准备阶段"

# 初始数据：1个纯绿色原链组成的DNA分子链（双链）
if 'dna_pool' not in st.session_state:
    st.session_state.dna_pool = [
        {
            "strand1": {"type": "original", "seq": "A T G C G T A C G T A"}, 
            "strand2": {"type": "original", "seq": "T A C G C A T G C A T"}
        }
    ]

# 2. 布局设置
col_micro, col_macro = st.columns([2, 1])

# ================= 左侧：微观动态变化 =================
with col_micro:
    st.subheader("🔬 微观：DNA 结构变化")
    
    st.markdown("<style>.tube{background-color:#f0f8ff;border:2px solid #add8e6;border-radius:10px;padding:15px;min-height:400px;}.dna-row{display:flex;flex-wrap:wrap;gap:15px;}.dna-card{background-color:#fff;border:1px solid #ccc;border-left:5px solid #4CAF50;padding:12px;border-radius:5px;font-family:monospace;font-size:16px;line-height:1.8;letter-spacing:1px;box-shadow:2px 2px 5px rgba(0,0,0,0.1);width:330px;}.seq-line{display:flex;justify-content:space-between;align-items:center;white-space:nowrap;margin:4px 0;}.green{color:#2e7d32;font-weight:bold;}.yellow{color:#d4a017;font-weight:bold;background-color:#fff3cd;padding:2px;border-radius:3px;}.red{color:#d62728;font-weight:bold;background-color:#fae6e6;padding:2px;border-radius:3px;}.separator{color:#aaa;font-size:12px;text-align:center;margin:2px 0;}</style>", unsafe_allow_html=True)
    
    html_micro = "<div class='tube'><div class='dna-row'>"
    
    def render_strand(strand):
        if strand['type'] == 'original':
            return f"<span class='green'>{strand['seq']}</span>"
        elif strand['type'] == 'hybrid':
            return f"<span class='yellow'>[{strand['primer']}]</span><span class='red'>{strand['ext']}</span>"
        elif strand['type'] == 'pure_new':
            return f"<span class='red'>{strand['seq']}</span>"

    if st.session_state.phase == "变性":
        st.markdown("<div style='color: #ff9800; font-weight: bold; margin-bottom: 10px;'>💥 90℃以上：氢键断裂，双链解开</div>", unsafe_allow_html=True)
        # 🚨 修改点 1：上限改成 8
        for i, dna in enumerate(st.session_state.dna_pool[:8]):
            html_micro += f"<div class='dna-card' style='border-left-color:#ff9800;'><div style='color:#888;'>DNA分子链 {i+1} 解链</div>"
            html_micro += f"<div class='seq-line'><span>5'</span> <span>{render_strand(dna['strand1'])}</span> <span>3'</span></div><div class='separator'>-- 氢键断裂 --</div><div class='seq-line'><span>3'</span> <span>{render_strand(dna['strand2'])}</span> <span>5'</span></div>"
            html_micro += "</div>"
    else:
        # 🚨 修改点 2：上限改成 8
        for i, dna in enumerate(st.session_state.dna_pool[:8]):
            html_micro += f"<div class='dna-card'><div style='color:#888;'>DNA分子链 {i+1}</div>"
            html_micro += f"<div class='seq-line'><span>5'</span> <span>{render_strand(dna['strand1'])}</span> <span>3'</span></div><div class='separator'>| | | | | | | | | | |</div><div class='seq-line'><span>3'</span> <span>{render_strand(dna['strand2'])}</span> <span>5'</span></div>"
            html_micro += "</div>"

    html_micro += "</div></div>"
    st.markdown(html_micro, unsafe_allow_html=True)
    
    # 🚨 修改点 3：提示文字同步改
    if len(st.session_state.dna_pool) > 8:
        st.write(f"... (还有 {len(st.session_state.dna_pool) - 8} 个 DNA 分子链未展示)")

# ================= 右侧：宏观数量与统计 =================
with col_macro:
    st.subheader("📊 宏观：DNA分子链数量统计")
    st.metric(label="🔄 当前延伸次数", value=f"第 {st.session_state.cycle} 轮")
    st.metric(label="🧬 试管内 DNA 分子链总数", value=f"{len(st.session_state.dna_pool)} 条（双链）")
    
    st.write("---")
    
    chain_has_original = 0 
    chain_hybrid = 0       
    chain_pure_new = 0     
    
    for dna in st.session_state.dna_pool:
        t1 = dna["strand1"]["type"]
        t2 = dna["strand2"]["type"]
        
        if t1 == "original" or t2 == "original":
            chain_has_original += 1
            
        if t1 == "hybrid" or t2 == "hybrid":
            chain_hybrid += 1
            
        if t1 == "pure_new" and t2 == "pure_new":
            chain_pure_new += 1

    st.success(f"🟢 含有原DNA链碱基的：**{chain_has_original} 条**")
    st.warning(f"🟡 含有引物的杂种链：**{chain_hybrid} 条**")
    st.error(f"🔴 完全由环境碱基组成的：**{chain_pure_new} 条**")

    st.write("---")
    st.write("**宏观图景（每块代表 1 条DNA分子链）：**")
    html_blocks = "<div style='display:flex;flex-wrap:wrap;gap:5px;'>"
    for dna in st.session_state.dna_pool:
        t1 = dna["strand1"]["type"]
        t2 = dna["strand2"]["type"]
        if t1 == "original" or t2 == "original":
            html_blocks += "<div style='width:16px;height:16px;background-color:#2e7d32;border-radius:2px;' title='含原链'></div>"
        elif t1 == "hybrid" or t2 == "hybrid":
            html_blocks += "<div style='width:16px;height:16px;background-color:#d4a017;border-radius:2px;' title='含引物杂合'></div>"
        else:
            html_blocks += "<div style='width:16px;height:16px;background-color:#d62728;border-radius:2px;' title='纯新链'></div>"
    html_blocks += "</div>"
    st.markdown(html_blocks, unsafe_allow_html=True)

# ================= 底部：操作按钮 =================
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🔥 1. 变性 (90℃以上)"):
        st.session_state.phase = "变性"
        st.rerun()

with col2:
    if st.button("❄️ 2. 复性 (50℃左右)"):
        if st.session_state.phase != "变性":
            st.error("❌ 错误：必须先经过变性解开双链！")
        else:
            st.session_state.phase = "复性"
            st.rerun()

with col3:
    if st.button("⚙️ 3. 延伸 (72℃左右)"):
        if st.session_state.phase != "复性":
            st.error("❌ 错误：引物还没结合，不能延伸！")
        else:
            st.session_state.phase = "延伸"
            st.session_state.cycle += 1
            
            new_pool = []
            for dna in st.session_state.dna_pool:
                # 1. 第一条链做模板
                s1 = dna["strand1"]
                if s1["type"] == "original":
                    new_pool.append({"strand1": s1, "strand2": {"type": "hybrid", "primer": "T A C G", "ext": "C A T G C A T"}})
                elif s1["type"] == "hybrid":
                    new_pool.append({"strand1": s1, "strand2": {"type": "pure_new", "seq": "G C A T G C A T G C A"}})
                else:
                    new_pool.append({"strand1": s1, "strand2": {"type": "pure_new", "seq": "C G T A C G T A C G T"}})
                
                # 2. 第二条链做模板
                s2 = dna["strand2"]
                if s2["type"] == "original":
                    new_pool.append({"strand1": s2, "strand2": {"type": "hybrid", "primer": "A T G C", "ext": "G T A C G T A"}})
                elif s2["type"] == "hybrid":
                    new_pool.append({"strand1": s2, "strand2": {"type": "pure_new", "seq": "C G T A C G T A C G T"}})
                else:
                    new_pool.append({"strand1": s2, "strand2": {"type": "pure_new", "seq": "G C A T G C A T G C A"}})
            
            st.session_state.dna_pool = new_pool
            st.rerun()

st.divider()
if st.button("🔄 重置实验"):
    st.session_state.cycle = 0
    st.session_state.phase = "准备阶段"
    st.session_state.dna_pool = [
        {
            "strand1": {"type": "original", "seq": "A T G C G T A C G T A"}, 
            "strand2": {"type": "original", "seq": "T A C G C A T G C A T"}
        }
    ]
    st.rerun()
st.markdown(
    """
    <div style="
        position: fixed; 
        bottom: 40px; 
        left: 50%; 
        transform: translateX(-50%); 
        opacity: 0.3; 
        z-index: 9999; 
        font-size: 14px; 
        color: gray; 
        pointer-events: none;
        letter-spacing: 2px;
    ">
        © 诸葛先生
    </div>
    """,
    unsafe_allow_html=True
)
