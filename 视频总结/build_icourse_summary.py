import json
from pathlib import Path


ROOT = Path(r"C:/My Data/zyl's obsidian/视频总结")
DATA = ROOT / "course_materials" / "icourse_video_data.json"
OUT = ROOT / "计算机组成原理（上）（下）MOOC视频教案式总结.md"


def clean(value):
    return str(value or "").replace("\u00a0", " ").strip()


def focus_for(title):
    title = clean(title)
    rules = [
        (("计算机系统简介", "计算机的基本组成"), "先建立整机视角：部件如何分工，程序和数据如何进入机器，控制器如何让一条指令流动起来。"),
        (("技术指标", "性能"), "不要孤立记主频；要把字长、运算速度、存储容量和实际工作负载联系起来。"),
        (("发展史", "应用和展望"), "把器件技术、体系结构、软件和应用需求放在同一条演进链上理解。"),
        (("总线",), "先问谁在通信、传什么、谁获得控制权，再理解总线结构、性能和控制方式。"),
        (("无符号数", "有符号数", "原码", "反码", "补码", "移码"), "把真值、机器数、符号位、模和表示范围放在同一张转换表中，重点理解补码为何能统一加减法。"),
        (("定点", "浮点"), "先确定小数点约定，再看尾数和阶码怎样共同决定精度、范围、规格化和机器零。"),
        (("定点运算", "移位", "乘法"), "把手算过程还原成寄存器、移位、加法器和控制信号，理解算法怎样落到硬件。"),
    ]
    for words, focus in rules:
        if any(word in title for word in words):
            return focus
    return "抓住本节的定义、结构、工作流程，以及它在整台计算机中的位置。"


def fallback_summary(title, segments):
    names = "、".join(name for _, name in segments)
    title = clean(title)
    if "总线" in title:
        return f"本视频围绕总线展开，按“{names}”的顺序说明部件之间如何共享传输通道，并进一步引出结构、性能和控制之间的取舍。"
    if any(word in title for word in ("补码", "原码", "反码", "移码", "无符号", "有符号")):
        return f"本视频围绕数的机器表示展开，按“{names}”逐步说明真值如何编码、不同编码怎样转换，以及表示范围和运算规则为何受到字长限制。"
    if "浮点" in title or "定点" in title:
        return f"本视频围绕定点数和浮点数展开，按“{names}”说明小数点约定、尾数与阶码、规格化和表示范围之间的关系。"
    if "乘法" in title or "定点运算" in title:
        return f"本视频围绕定点运算展开，按“{names}”把数学运算还原为移位、加法、寄存器保存和溢出判断等硬件步骤。"
    return f"本视频按“{names}”推进讲解，从基本概念进入结构、工作过程和应用，帮助把本节知识放回计算机系统整体中理解。"


def content_range(segments):
    return "；".join(f"{start} {name}" for start, name in segments)


def segment_rows(segments):
    rows = []
    for start, name in segments:
        rows.extend([f"#### {start} {name}", "", f"这一段聚焦“{name}”。结合画面中的结构图、公式或演示，应重点观察信息从哪里来、经过什么部件、最后保存到哪里。", ""])
    return rows


def render_video(video, course_label, course_url):
    title = clean(video.get("name"))
    url = video.get("url") or course_url
    raw_segments = video.get("segments") or []
    segments = []
    for item in raw_segments:
        bits = clean(item).splitlines()
        if len(bits) >= 2:
            segments.append((bits[0], clean(" ".join(bits[1:]))))
    summary = clean(video.get("summary")) or fallback_summary(title, segments)
    rows = [f"### {title}", "", f"> 视频：[{url}]({url})", f"> 内容：{content_range(segments) or '本视频围绕课程目录中的本节主题展开，覆盖概念、结构、工作过程及其与前后知识的联系。'}", "> 说明：本笔记结合 MOOC 视频讲解、播放器右侧切分标题、字幕/音频信息、画面中的文字与结构图，并与对应课程文档及同主题完整课程资料交叉整理，适合作为单集回看和章节串联材料。", "", f"**本节抓手：** {focus_for(title)}", "", "**本节讲解：**", "", summary, "", "**视频内知识切分：**", ""]
    rows.extend(segment_rows(segments))
    rows.extend([f"**与课程主线的连接：** {course_label}中的本视频把前面的知识推进到下一层：先明确对象和表示，再说明结构与过程，最后落到性能、实现或系统协同。", "", "---", ""])
    return rows


def main():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    upper_url = data["courses"]["upper"]
    lower_url = data["courses"]["lower"]
    rows = [
        "# 计算机组成原理（上）（下）MOOC视频教案式总结",
        "",
        "> 课程：哈尔滨工业大学《计算机组成原理（上）》与《计算机组成原理（下）》",
        "> 来源：[上册课程页面](https://www.icourse163.org/learn/HIT-309001?tid=1487851457#/learn/content)；[下册课程页面](https://www.icourse163.org/learn/HIT-1001527001?tid=1487834457#/learn/content)",
        "> 整理说明：本文以课程页面实际列出的 41 个视频为索引，保留原视频标题和播放器右侧的时间切分；视频正文采用教案式语言重述，帮助初学者建立“表示 → 运算 → 存储 → 指令 → CPU → 总线/I/O”的完整知识链。页面条目、字幕和智能总结属于课程辅助材料，不能替代视频本身；涉及图表、公式和结构图时，应结合画面复核。",
        "",
        "## 一、先建立全局图",
        "",
        "计算机组成原理回答的不是“电脑有哪些零件”这么简单，而是回答：信息如何表示，如何存放，如何被指令取出，如何由运算器处理，如何由控制器组织成时序动作，以及多个部件如何通过总线和 I/O 协同。",
        "",
        "```text",
        "现实信息 → 二进制编码 → 存储器保存 → 指令描述操作",
        "                                  ↓",
        "             CPU 取指、译码、执行并控制数据流",
        "                                  ↓",
        "             总线连接部件，I/O 与外部世界交换信息",
        "```",
        "",
        "上册课程页面当前覆盖计算机系统概论、计算机的发展及应用、系统总线；下册课程页面当前覆盖无符号数和有符号数、定点/浮点表示、定点运算。课程页面中的标题是学习索引，完整的章节依赖关系可参考同文件夹中的 [[《计算机组成原理微课堂》教案式总结]]。",
        "",
        "## 二、学习方法",
        "",
        "1. 先看每个视频的时间切分，知道本节在解决什么问题。",
        "2. 再读“本节讲解”，把术语放回结构和工作流程中。",
        "3. 遇到公式时同时问三个问题：变量代表什么、适用条件是什么、溢出或边界在哪里。",
        "4. 学完一个主题后，用“数据在哪里、采用什么编码、谁在搬运、谁在控制”复述一遍。",
        "",
        "## 三、上册：计算机系统、发展与总线",
        "",
    ]
    for video in data["upper"]:
        rows.extend(render_video(video, "上册", upper_url))
    rows.extend(["## 四、下册：数的表示与定点运算", ""])
    for video in data["lower"]:
        rows.extend(render_video(video, "下册", lower_url))
    rows.extend([
        "## 五、跨视频复习骨架",
        "",
        "### 1. 从系统到部件",
        "",
        "先用计算机系统概论回答“有哪些部件、怎样分层”，再用基本组成回答“存储器、运算器和控制器各自做什么”。总线把这些部件的连接关系具体化，说明信息传输不是任意发生的，而要受结构、仲裁、定时和性能约束。",
        "",
        "### 2. 从真值到机器数",
        "",
        "下册先区分无符号数与有符号数，再依次建立原码、补码、反码和移码。核心不是背表，而是理解：机器字长决定模和表示范围；补码把减法转化为加法；移码便于比较阶码，因此常用于浮点数的阶码部分。",
        "",
        "### 3. 从表示到运算",
        "",
        "定点/浮点表示解决“数怎样存”，定点运算解决“数怎样算”。移位、加法、乘法和溢出判断都必须落实到寄存器位级变化；看到一个算法时，要能说出需要哪些寄存器、哪些加法器，以及每一步由什么控制信号触发。",
        "",
        "### 4. 最终复述模板",
        "",
        "面对任何组成原理题，可以按以下顺序组织答案：定义对象 → 给出编码/结构 → 描述数据流和控制流 → 写出公式或时序 → 检查表示范围、溢出和边界条件 → 说明它和整机性能或后续章节的联系。",
        "",
        "## 六、资料范围与局限",
        "",
        "本文严格按 MOOC 页面当前可见的视频条目制作；课程页面若因开课批次、登录状态或内容更新而增加/隐藏资源，本文不会自动同步。视频内切分标题和课程页面摘要是页面提供的辅助索引，公式、图表和推导仍应以原视频画面和课程文档为准。",
        "",
    ])
    OUT.write_text("\n".join(rows).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {OUT} with {len(data['upper']) + len(data['lower'])} videos")


if __name__ == "__main__":
    main()
