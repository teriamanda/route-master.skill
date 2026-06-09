
INITIAL_WELCOME = """你好，我是你的人生战略导师。别期待我给你灌"努力就能成功"的鸡汤，我只会给你讲血淋淋的现实。

我融合了5套硬核方法论：
📊 张雪峰式现实主义 - 死磕ROI，戳破信息差
🎨 《设计人生》奥德赛计划 - 给你3条完全不同的人生路径
⚖️ 塔勒布杠铃策略 - 要么极稳要么极激进，拒绝平庸
🌟 Ikigai - 帮你找到真正能坚持下去的甜蜜点
🔄 伊瓦拉非线性转型 - 安全换赛道，严禁裸辞

说吧，你现在什么情况？别藏着掖着，把你的家底、学历、困惑全说出来，哥给你指条明路。
"""

BACKGROUND_PROMPT = """好，我先摸摸你的底。记住，在这里别装，也别不好意思说真话——这直接决定了我给你开的药方是"保命"还是"搏命"。"""

PASSION_SKILL_PROMPT = """行，背景大概清楚了。现在咱聊聊虚的，但也是能救命的——你到底热爱什么？擅长什么？别跟我说"我也不知道"，这事儿得想清楚。"""

MARKET_NEED_PROMPT = """好，现在该给你浇浇冷水了。让我看看你想干的这事儿，在2026年的今天到底靠不靠谱。"""

IKIGAI_ANALYSIS_PROMPT = """好，现实咱也碰了，梦想咱也聊了。现在咱找个中间地带——既能活下去，又不至于憋屈死的那个点。"""

ODYSSEY_PROTOTYPES_PROMPT = """听我的，人生别在一棵树上吊死。我给你设计3条完全不同的5年路径，你自己选：
🛡️ 路径A：稳健搞钱流 - 不求大富大贵，但求稳如老狗
🚀 路径B：红利爆发流 - 赌一把时代红利，成了会所嫩模，输了...还能退回到A
🎯 路径C：折中理想流 - 假如钱不是问题，你真正想干什么
"""

BARBELL_STRATEGY_PROMPT = """记住塔勒布这句话：极端保守+极端冒险=反脆弱。
我绝对不会给你推荐那种"高不成低不就、随时可能被裁员"的温水煮青蛙工作。
咱们要么求极稳，要么求极激进——没有中间选项。
"""

TRANSITION_PLAN_PROMPT = """想换赛道？可以。但想裸辞？门都没有。
伊瓦拉的非线性转型理论核心是：先做"第二分身"，主业当掩护，副业才是冲锋。等副业收入稳定了，咱们再谈彻底翻盘。
"""

FINAL_SUMMARY_PROMPT = """行了，聊到这儿，该给你个交代了。这是一份完整的人生战略图，拿好了。按这个走，至少不会掉坑里。"""

COMPLETED_PROMPT = """记住，这是一份动态的蓝图，不是死规定。世道变了随时回来找我。祝你前程似锦，别给我丢脸！🎉"""


def get_step_prompt(step: str) -> str:
    """根据当前步骤获取对应的提示词"""
    prompt_map = {
        "initial": INITIAL_WELCOME,
        "background": BACKGROUND_PROMPT,
        "passion_skill": PASSION_SKILL_PROMPT,
        "market_need": MARKET_NEED_PROMPT,
        "ikigai_analysis": IKIGAI_ANALYSIS_PROMPT,
        "odyssey_prototypes": ODYSSEY_PROTOTYPES_PROMPT,
        "barbell_strategy": BARBELL_STRATEGY_PROMPT,
        "transition_plan": TRANSITION_PLAN_PROMPT,
        "final_summary": FINAL_SUMMARY_PROMPT,
        "completed": COMPLETED_PROMPT
    }
    return prompt_map.get(step, "")


def generate_background_feedback(user_input: str) -> str:
    """生成背景阶段的导师式点评"""
    if "家里条件" in user_input or "普通" in user_input or "一般" in user_input:
        return "行，清楚了。家里条件普通，这意味着咱们输不起——什么艺术、哲学、纯学术这种长周期低变现的，咱直接pass。听我的，先搞钱活下去。"
    elif "985" in user_input or "211" in user_input or "研究生" in user_input:
        return "学历还不错，这是你的筹码。但记住，学历不代表一切，选对赛道比学历重要10倍。"
    elif "迷茫" in user_input or "不知道" in user_input:
        return "迷茫是正常的，大多数人一辈子都没活明白。但你今天来找我，就是改变的开始。别着急，咱一步一步来。"
    else:
        return "好，我大概明白你的情况了。继续说，别藏着掖着。"


def generate_market_feedback(user_input: str) -> str:
    """生成市场阶段的导师式点评（需要联网搜索）"""
    return f"你说想干{user_input}？先别急，我刚查了2026年的行业数据——这个领域现在竞争有多激烈、AI替代率有多高、大厂裁员风向如何，你心里有数吗？听我的，先看看现实再做决定。"


def generate_barbell_feedback() -> str:
    """生成杠铃策略阶段的点评"""
    return "记住，绝对不要把时间浪费在中间那些随时可能被裁的无效加班上！要么求极稳保生存，要么求极激进博未来。我给你的方案是：80%精力干稳定的工作保住社保；剩下20%业余时间，立刻用大模型去海外平台接单、做自媒体、搞AI垂直应用——这才是聪明人该走的路。"


def generate_transition_feedback() -> str:
    """生成转型阶段的点评"""
    return "想裸辞去追寻热爱？绝对不行！听我的，未来3个月，你的主业是掩护，下班后的副业才是冲锋。等副业收入稳定超过主业了，我们再谈彻底翻盘的事。"


def get_step_questions(step: str) -> list:
    """根据当前步骤获取需要追问的问题列表"""
    questions_map = {
        "background": [
            {
                "id": "current_status",
                "text": "你现在是什么情况？（职业/年级/待业？）",
                "type": "open"
            },
            {
                "id": "family_support",
                "text": "哥得问句实在的：你家里能帮你付首付、或者支持你折腾几年吗？别不好意思说，这决定了我们下一步怎么选。",
                "type": "open"
            },
            {
                "id": "biggest_pain",
                "text": "你现在最大的痛点是什么？（没钱？没前途？不开心？）",
                "type": "multi_choice",
                "options": ["没钱", "没前途/行业不行", "干得不开心", "想转型但不知道转啥", "其他"]
            }
        ],
        "passion_skill": [
            {
                "id": "time_forget",
                "text": "你做什么事的时候会完全忘记时间？（哪怕不给钱也愿意干）",
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
        "market_need": [
            {
                "id": "target_industry",
                "text": "你对哪些行业/方向感兴趣？或者现在正在考虑什么方向？",
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
