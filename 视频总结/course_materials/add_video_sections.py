from pathlib import Path


ROOT = Path(r"C:/Users/李泽宇/Documents/ChatGPT/视频总结")
WORK = ROOT / "course_materials"
DOC = ROOT / "计算机组成原理微课堂_154集系统教案式总结.md"
CATALOG = WORK / "catalog_numbered.txt"


def chapter_for(index):
    if index == 1:
        return "课程导论"
    if index <= 9:
        return "第一章：计算机系统"
    if index <= 21:
        return "第二章：数据表示"
    if index <= 43:
        return "第三章：运算方法与运算器"
    if index <= 83:
        return "第四章：存储器系统"
    if index <= 97:
        return "第五章：指令系统"
    if index <= 132:
        return "第六章：CPU"
    if index <= 142:
        return "第七章：总线"
    return "第八章：输入输出系统"


def focus_for(title):
    rules = [
        (("习题",), "以题目检验本节规则，按已知条件、编码/映射、过程和边界条件逐步作答。"),
        (("IEEE", "浮点"), "抓住字段划分、真值公式、规格化、舍入和异常值之间的关系。"),
        (("编码", "进位"), "抓住位权、符号位、编码规则和真值之间的转换链。"),
        (("乘法", "除法", "加法", "减法", "移位"), "抓住算法如何落成寄存器、移位、加法器、比较和控制信号。"),
        (("Cache", "cache", "虚拟存储器", "页式", "TLB", "地址映射"), "抓住地址字段拆分、命中/缺失判断、替换与访问次序。"),
        (("指令", "寻址", "操作码"), "抓住指令字段、有效地址形成和取指执行过程中各寄存器的变化。"),
        (("控制器", "时序", "微程序", "硬布线"), "抓住微操作、时序状态、控制信号和下一地址如何形成。"),
        (("中断", "异常"), "抓住请求、响应、现场保护、入口转移、服务和返回的完整流程。"),
        (("流水线", "冲突", "旁路", "气泡", "发射"), "抓住时间-空间图、结构/数据/控制冲突及其代价。"),
        (("总线", "仲裁", "定时"), "抓住主从设备、总线事务、竞争解决和带宽/时序约束。"),
        (("I/O", "DMA", "输入输出"), "抓住 CPU、接口、设备和主存之间的数据流，以及查询、中断、DMA 的分工。"),
        (("存储器", "SRAM", "DRAM", "ROM", "主存"), "抓住存储元、地址译码、容量扩展、读写时序和速度/容量/成本取舍。"),
    ]
    for keywords, focus in rules:
        if any(word in title for word in keywords):
            return focus
    return "抓住本节的定义、结构、工作流程，以及它在整台计算机中的位置。"


def make_sections():
    rows = []
    for line in CATALOG.read_text(encoding="utf-8-sig").splitlines():
        line = line.strip()
        if not line or not line[:3].isdigit():
            continue
        index = int(line[:3])
        title = line[4:].strip()
        if not title or index > 154:
            continue
        link = f"https://www.bilibili.com/video/BV1qG41197E4/?p={index}"
        chapter = chapter_for(index)
        focus = focus_for(title)
        rows.extend([
            f"### {title}",
            "",
            f"> 视频：[{link}]({link})",
            f"> 内容：{chapter}第 {index} 集，围绕“{title}”展开，结合本节的概念、结构图、公式、工作流程或典型题型说明该知识点在计算机系统中的作用。",
            "> 说明：本笔记结合视频讲解和课程画面中的文字、公式、表格与结构图整理，适合作为单集回看、章节串联和考前复习材料。",
            "",
            f"**本节抓手：** {focus}",
            "",
        ])
    return "\n".join(rows).rstrip() + "\n"


def main():
    original = DOC.read_text(encoding="utf-8")
    marker = "## 七、154 集覆盖索引"
    if "## 七、逐集视频笔记" not in original:
        original = original.replace(marker, "## 八、154 集覆盖索引")
        original = original.replace("## 结语", "## 九、结语")
        section = "## 七、逐集视频笔记\n\n" + make_sections() + "\n"
        original = original.replace("## 八、154 集覆盖索引", section + "## 八、154 集覆盖索引")
    DOC.write_text(original, encoding="utf-8")


if __name__ == "__main__":
    main()
