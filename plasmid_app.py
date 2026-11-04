import streamlit as st
from PIL import Image # 引入PIL读取图片

st.set_page_config(layout="wide", page_title="研发员实战：选酶与改造")
st.title("🏭 研发员实战：构建重组载体与 PCR 改造")
st.write("请仔细观察左侧的**质粒载体**和**S基因**图谱，先在右侧完成限制酶的选择，然后回答下方的进阶考题。")

# 初始化记忆状态（记录是否成功切割，防止刷新丢失）
if 'cleavage_success' not in st.session_state:
    st.session_state.cleavage_success = False

col_left, col_right = st.columns([1.2, 1])

# ================= 左侧：图片展示区 =================
with col_left:
    st.subheader("🔬 实验台图谱")
    
    try:
        # 读取同目录下的本地图片，并固定宽度为 800，防止云端排版卡死
        image = Image.open("plasmid_map.png")
        st.image(image, caption="质粒载体与S基因图谱", width=800)
    except Exception as e:
        st.error(f"⚠️ 找不到或无法读取图片。请确保图片名为 plasmid_map.png 且与代码在同一文件夹。错误信息：{e}")

# ================= 右侧：互动操作区 =================
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
        st.success("✅ 切割成功！你找到了位于启动子和终止子之间的两个安全切点（EcoR I 和 Xba I）。")
        st.markdown("---")
        st.subheader("📝 第二步：PCR 引物改造")
        st.write("虽然载体切开了，但是！**S基因内部也含有 Xba I 切点**，如果直接用扩增产物去切，S基因还是会断！")
        st.info("👨‍🔬 提示：我们在 PCR 扩增 S 基因时，可以通过设计引物来“无中生有”地加上接头！")
        
        # 表单区：只负责收集数据
        with st.form("question_form"):
            q1 = st.radio("（1）PCR扩增S基因时，需在引物的哪一端添加限制酶识别序列？", ["5'端", "3'端"], horizontal=True)
            q2 = st.text_input("（2）结合上表分析，上游引物应添加的碱基序列是5'-_________-3'（只填英文字母）：")
            submit = st.form_submit_button("提交答案")

        # 判定区：在表单外部接收结果，确保能正常渲染反馈
        if submit:
            if q1 == "5'端":
                st.success("✅ 第(1)题正确！PCR扩增时，新链是从引物的 3' 端开始延伸的，所以接头必须加在引物的 5' 端。")
            else:
                st.error("❌ 第(1)题错误！加在 3' 端的话，DNA聚合酶就没法延伸了。")
                
            clean_q2 = q2.replace(" ", "").upper()
            if clean_q2 == "GAATTC":
                st.success("✅ 第(2)题正确！上游引物需要添加 EcoR I 的识别序列 GAATTC。")
                st.balloons()
                st.write("### 🎉 太棒了！你完美掌握了引物改造的技巧！")
            else:
                st.error(f"❌ 第(2)题错误。你的输入是：{clean_q2}，请仔细查看左侧表格中 EcoR I 的识别序列。")
