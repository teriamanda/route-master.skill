
# 融合《设计人生》方法论的导师提示词

INITIAL_WELCOME = """你好，我是你的人生战略导师。别期待我给你灌"努力就能成功"的鸡汤，我只会给你讲血淋淋的现实——但这次，我们先用《斯坦福大学人生设计课》的方法论，先花点时间好好认识你自己。

我融合了5套硬核方法论：
📊 张雪峰式现实主义 - 死磕ROI，戳破信息差
🎨 《设计人生》奥德赛计划 - 给你3条完全不同的人生路径
⚖️ 塔勒布杠铃策略 - 要么极稳要么极激进，拒绝平庸
🌟 Ikigai - 帮你找到真正能坚持下去的甜蜜点
🔄 伊瓦拉非线性转型 - 安全换赛道，严禁裸辞

这次我们的流程是：
1️⃣ 先搞清楚你的人生观和工作观（《设计人生》核心）
2️⃣ 再看看你的热爱和擅长
3️⃣ 然后给你看现实的市场情况
4️⃣ 最后给你设计3种人生版本和杠铃策略

说吧，你现在什么情况？别藏着掖着，把你的家底、学历、困惑全说出来，哥给你指条明路。
"""

# --- 《设计人生》方法论相关 ---

LIFE_WORK_VIEW_INTRO = """好，我们正式开始。在想干什么之前，先想想怎么活。这是《设计人生》里最重要的第一步——我们需要让你的人生观和工作观对齐，这才能真正幸福。"""

LIFE_VIEW_QUESTION = """📌 首先是**人生观**：
1. 对你来说，人生中最重要的是什么？（比如：家庭、健康、成就感、自由、学习、帮助别人...）
2. 想象你80岁的时候，回顾一生，你希望自己是怎么度过的？
3. 你认为'成功'是什么？（有钱？有名？有意义？还是别的？）
"""

WORK_VIEW_QUESTION = """📌 接下来是**工作观**：
1. 工作为什么重要？对你来说，工作是为了什么？（赚钱？成长？实现价值？打发时间？）
2. 你理想中的'好工作'是什么样的？（氛围？同事？内容？时间？薪资？）
3. 你绝对不想在工作中忍受什么？（比如：熬夜加班？办公室政治？没有成长？）
"""

PROBLEM_FRAMING_INTRO = """好的，我把你的人生观和工作观记下来了。这两个'观'越一致，你就会越幸福。

现在是《设计人生》里最神奇的一步——**问题重构**。很多时候我们问错了问题，比如'我应该选什么工作？'，但更好的问题是'如何能够找到既赚钱又有意义的事？'

我们来重新定义你的问题。
"""

WAYFINDING_INTRO = """很好！你把问题重新定义了。现在，我们来找找你的**能量来源**。这是《设计人生》里的'方向探索'（Wayfinding）。

做什么让你满血复活？做什么让你精疲力尽？我们要多做给你能量的事，少做消耗你的事。
"""

ODYSSEY_INTRO = """太棒了！现在我们来到《设计人生》的招牌环节——**奥德赛计划**！

记住：人生不止一条路。我们来设计3种完全不同的5年人生版本，你不用现在就选，但你要知道你有选择。
"""

# --- 反馈函数 ---

def generate_background_feedback(user_input: str) -> str:
    feedback = "好，我了解你的基本情况了。"
    if "普通" in user_input or "一般" in user_input or "没什么钱" in user_input:
        feedback += "家里条件普通是吧？没关系，这说明我们输不起，必须走最稳妥、ROI最高的路线。那些什么艺术、哲学、纯学术的，咱直接pass。先搞钱活下去，再谈理想。"
    feedback += "\n\n现在，在想干什么之前，我们先用《设计人生》的方法论，先搞清楚你的人生观和工作观。这很重要——只有这两个'观'对齐了，你才会真正幸福。"
    return feedback

def generate_life_view_feedback(user_input: str) -> str:
    return "有意思！你的人生观是这样的...记下来了。现在我们来聊聊工作观——工作对你意味着什么？"

def generate_work_view_feedback(user_input: str) -> str:
    return "好！工作观也记录下来了。我们继续。"

def generate_passion_skill_feedback(user_input: str) -> str:
    return "有意思！这些信息很重要——你的热情和擅长是我们设计人生的原材料。现在该给你浇点冷水了——让我们看看市场的真实情况，张雪峰式的现实分析要来了。"

def generate_market_feedback(user_input: str) -> str:
    return f"你说想干{user_input}？先别急，我刚查了2026年的行业数据——这个领域现在竞争有多激烈、AI替代率有多高、大厂裁员风向如何，你心里有数吗？听我的，先看看现实再做决定。\n\n不过别灰心，现实虽然骨感，但咱得找个平衡点。我们现在来做Ikigai分析，找到你的甜蜜点。"

def generate_ikigai_feedback() -> str:
    return "好，甜蜜点咱也找到了。但人生不能只选一条路，我给你设计3条完全不同的5年路径——这就是《设计人生》里的奥德赛计划！"

def generate_odyssey_feedback() -> str:
    feedback = "好！3条人生路径都设计出来了。现在该上塔勒布的杠铃策略了。\n"
    feedback += "记住：绝对不要把时间浪费在中间那些随时可能被裁的无效加班上！要么极稳保生存，要么极激进博未来。\n"
    feedback += "我给你的方案是：80%精力干稳定的工作保住社保；剩下20%业余时间，立刻用AI工具去海外平台接单、搞内容、做垂直应用——这才是聪明人该走的路。"
    return feedback

def generate_barbell_feedback() -> str:
    feedback = "想裸辞去追寻热爱？绝对不行！伊瓦拉的非线性转型理论核心是：先做'第二分身'，主业当掩护，副业才是冲锋。等副业收入稳定超过主业了，我们再谈彻底翻盘的事。"
    return feedback

def generate_final_feedback() -> str:
    return "行了，聊到这儿，该给你个交代了。这是一份完整的人生战略图，拿好了。按这个走，至少不会掉坑里。记住：这是动态的蓝图，世道变了随时回来调整。祝你前程似锦，别给我丢脸！🎉"

# --- 问题生成函数 ---

def get_step_questions(step: str) -> list:
    """根据当前步骤获取需要追问的问题列表"""
    questions_map = {
        "background": [
            {
                "id": "current_status",
                "text": "你目前从事什么职业/在上学几年级？",
                "type": "open"
            },
            {
                "id": "family_support",
                "text": "哥得问句实在的：你家里能帮你付首付、或者支持你折腾几年吗？别不好意思说，这决定了我们是'保命'还是'搏命'。",
                "type": "open"
            },
            {
                "id": "biggest_pain",
                "text": "你现在最大的痛点是什么？（没钱/没前途/干得不开心/想转型）",
                "type": "multi_choice",
                "options": ["没钱", "没前途/行业不行", "干得不开心", "想转型但不知道转啥", "其他"]
            }
        ],
        "life_view": [
            {
                "id": "life_priority",
                "text": "对你来说，人生中最重要的是什么？（比如：家庭、健康、成就感、自由、学习、帮助别人...）",
                "type": "open"
            },
            {
                "id": "80_year_old",
                "text": "想象你80岁的时候，回顾一生，你希望自己是怎么度过的？",
                "type": "open"
            },
            {
                "id": "success_definition",
                "text": "你认为'成功'是什么？（有钱？有名？有意义？还是别的？）",
                "type": "open"
            }
        ],
        "work_view": [
            {
                "id": "work_purpose",
                "text": "工作为什么重要？对你来说，工作是为了什么？（赚钱？成长？实现价值？打发时间？）",
                "type": "open"
            },
            {
                "id": "ideal_job",
                "text": "你理想中的'好工作'是什么样的？（氛围？同事？内容？时间？薪资？）",
                "type": "open"
            },
            {
                "id": "deal_breakers",
                "text": "你绝对不想在工作中忍受什么？（比如：熬夜加班？办公室政治？没有成长？）",
                "type": "open"
            }
        ],
        "problem_framing": [
            {
                "id": "current_problem",
                "text": "你现在最想解决的问题是什么？（比如：'我要转行'、'我不知道做什么'、'我想赚更多钱'...）",
                "type": "open"
            },
            {
                "id": "why_problem_matters",
                "text": "这个问题背后，你真正想要的是什么？（比如：'转行'背后可能是想要更多掌控感、更多可能性...）",
                "type": "open"
            },
            {
                "id": "how_might_we",
                "text": "如果用'如何能够...'来重新定义，你的问题会变成什么？（比如：'如何能够找到既赚钱又有意义的事？'）",
                "type": "open"
            }
        ],
        "passion_skill": [
            {
                "id": "time_forget",
                "text": "你做什么事情的时候会完全忘记时间？（哪怕不给钱也愿意干）",
                "type": "open"
            },
            {
                "id": "others_praise",
                "text": "别人经常夸你什么？（别谦虚，实话实说）",
                "type": "open"
            },
            {
                "id": "learn_willing",
                "text": "如果不考虑钱，你愿意花时间学什么？",
                "type": "open"
            }
        ],
        "wayfinding": [
            {
                "id": "energy_gain",
                "text": "回想你过去做过的事，做什么的时候你最投入、最开心、甚至忘记时间？",
                "type": "open"
            },
            {
                "id": "authentic_self",
                "text": "做什么事让你觉得'这才是我'？",
                "type": "open"
            },
            {
                "id": "energy_drain",
                "text": "反过来，做什么让你觉得特别消耗、不想再做？",
                "type": "open"
            }
        ],
        "market_need": [
            {
                "id": "target_industry",
                "text": "你对哪些行业或方向感兴趣？或者现在正在考虑做什么？",
                "type": "open"
            },
            {
                "id": "risk_tolerance",
                "text": "你能接受的风险程度？",
                "type": "single_choice",
                "options": ["极度保守 - 只求稳定", "偏保守 - 可以小赌", "中性 - 富贵险中求", "激进 - 搏一把大的"]
            }
        ],
        "ikigai_analysis": [],
        "odyssey_prototypes": [],
        "barbell_strategy": [],
        "transition_plan": [],
        "final_summary": [],
        "completed": []
    }
    return questions_map.get(step, [])

