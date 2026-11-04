import streamlit as st

st.set_page_config(layout="wide", page_title="研发员实战：选酶与改造")
st.title("🏭 研发员实战：构建重组载体与 PCR 改造")

# 初始化记忆状态（记录是否成功切割）
if 'cleavage_success' not in st.session_state:
    st.session_state.cleavage_success = False

col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("🔬 实验台图谱")
    try:
        st.image("plasmid_map.png", caption="质粒载体与S基因图谱", use_container_width=True)
    except FileNotFoundError:
       st.error("⚠️ 找不到图片！请确保图片命名为 'plasmid_map.png' 并且和代码文件放在了同一个文件夹里。")

with col_right:
    st.subheader("✂️ 第一步：限制酶选择区")
    st.info("💡 **研发提示**：双酶切可以防反向连接，但要注意不要切断S基因内部！")
    
    enzymes = st.multiselect(
        "请从酶库中选择（建议选2个）：",
        ["Bgl II", "Nde I", "Xho I", "EcoR I", "BamH I", "Sal I", "Xba I"]
    )
    
    if st.button("🚀 执行切割与连接", use_container_width=True):
        if len(enzymes) == 0:
            st.warning("请先选择限制酶！")
        elif "BamH I" in enzymes or "Nde I" in enzymes:
            st.error("❌ 失败！你在S基因内部有切点，图纸被切碎了！")
        elif len(enzymes) == 1:
            st.error("❌ 失败！单酶切会导致自身环化或反向连接！")
        elif "EcoR I" in enzymes and "Xba I" in enzymes and len(enzymes) == 2:
            # 如果选对了，把记忆状态设为 True
            st.session_state.cleavage_success = True
        else:
            st.error("❌ 方案不可行，请重新审视图谱，寻找正确的双酶切组合！")

# 如果第一步选酶成功了，才会显示下面的进阶题
if st.session_state.cleavage_success:
    with col_right:
        st.success("✅ 切割成功！你找到了位于启动子和终止子之间的两个安全切点（EcoR I 和 Xba I）。")
        st.markdown("---")
        st.subheader("📝 第二步：PCR 引物改造")
        st.write("虽然载体切开了，但是！**S基因内部也含有 Xba I 切点**，如果直接用扩增产物去切，S基因还是会断！")
        st.info("👨‍🔬 提示：我们在 PCR 扩增 S 基因时，可以通过设计引物来“无中生有”地加上接头！")
        
        # 表单区
        with st.form("question_form"):
            q1 = st.radio("（1）PCR扩增S基因时，需在引物的哪一端添加限制酶识别序列？", ["5'端", "3'端"], horizontal=True)
            q2 = st.text_input("（2）结合上表分析，上游引物应添加的碱基序列是5'-_________-3'（只填英文字母）：")
            submit = st.form_submit_button("提交答案")

        # 表单反馈区（在 with 外面）
        if submit:
            # 判定方向
            if q1 == "5'端":
                st.success("✅ 第(1)题正确！PCR扩增时，新链是从引物的 3' 端开始延伸的，所以接头必须加在引物的 5' 端。")
            else:
                st.error("❌ 第(1)题错误！加在 3' 端的话，DNA聚合酶就没法延伸了。")
                
            # 判定序列
            clean_q2 = q2.replace(" ", "").upper()
            if clean_q2 == "GAATTC":
                st.success("✅ 第(2)题正确！上游引物需要添加 EcoR I 的识别序列 GAATTC。")
                st.balloons()
            else:
                st.error(f"❌ 第(2)题错误。你的输入是：{clean_q2}，请仔细查看左侧表格中 EcoR I 的识别序列。")
