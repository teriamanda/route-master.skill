from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from typing import List, Optional, Dict, Any, Literal
from enum import Enum
import prompts

app = FastAPI(title="人生战略级导师智能体", version="3.0.0")


class QuestionType(str, Enum):
    OPEN = "open"
    SINGLE_CHOICE = "single_choice"
    MULTI_CHOICE = "multi_choice"


class Step(str, Enum):
    INITIAL = "initial"
    BACKGROUND = "background"
    PASSION_SKILL = "passion_skill"
    MARKET_NEED = "market_need"
    IKIGAI_ANALYSIS = "ikigai_analysis"
    ODYSSEY_PROTOTYPES = "odyssey_prototypes"
    BARBELL_STRATEGY = "barbell_strategy"
    TRANSITION_PLAN = "transition_plan"
    FINAL_SUMMARY = "final_summary"
    COMPLETED = "completed"


class VisualType(str, Enum):
    IKIGAI_RADAR = "ikigai_radar"
    BARBELL_SIMULATOR = "barbell_simulator"
    ODYSSEY_TIMELINE = "odyssey_timeline"
    NONE = "none"


class Question(BaseModel):
    id: str = Field(..., description="问题唯一标识")
    text: str = Field(..., description="问题文本")
    type: QuestionType = Field(..., description="问题类型")
    options: Optional[List[str]] = Field(None, description="选项列表（仅用于单选/多选）")


class State(BaseModel):
    current_step: Step = Field(..., description="当前会话步骤")
    user_profile: Dict[str, Any] = Field(default_factory=dict, description="用户画像数据")
    collected_data: Dict[str, Any] = Field(default_factory=dict, description="对话过程中收集的信息")


class IkigaiData(BaseModel):
    """Ikigai 雷达图数据结构"""
    passion_score: int = Field(..., ge=0, le=100, description="热情维度评分 0-100")
    skill_score: int = Field(..., ge=0, le=100, description="擅长维度评分 0-100")
    market_score: int = Field(..., ge=0, le=100, description="市场需求维度评分 0-100")
    reward_score: int = Field(..., ge=0, le=100, description="回报维度评分 0-100")
    sweet_spot: List[str] = Field(default_factory=list, description="甜蜜点标签列表")
    high_risk_areas: List[str] = Field(default_factory=list, description="高危盲区标签列表")
    ai_replacement_risk: int = Field(..., ge=0, le=100, description="AI替代风险评分 0-100")


class BarbellSide(BaseModel):
    """杠铃单一侧数据结构"""
    name: str = Field(..., description="该侧名称")
    description: str = Field(..., description="该侧描述")
    risk_score: int = Field(..., ge=0, le=100, description="风险评分 0-100（防守侧越低越好）")
    base_return: float = Field(..., ge=0, description="基础年化收益/月薪")
    allocation_percent: int = Field(..., ge=0, le=100, description="分配比例 0-100")
    examples: List[str] = Field(default_factory=list, description="具体例子")


class BarbellData(BaseModel):
    """杠铃策略模拟器数据结构"""
    left_side: BarbellSide = Field(..., description="左侧：防守池")
    right_side: BarbellSide = Field(..., description="右侧：进攻池")
    total_risk_score: int = Field(..., ge=0, le=100, description="整体风险评分")
    mentor_note: str = Field(..., description="导师备注")


class OdysseyMilestone(BaseModel):
    """奥德赛单个里程碑节点"""
    time_point: str = Field(..., description="时间节点：3months, 6months, 1year, 3years, 5years")
    title: str = Field(..., description="里程碑标题")
    description: str = Field(..., description="里程碑详细描述")
    actions: List[str] = Field(default_factory=list, description="具体行动列表")
    success_criteria: str = Field(..., description="成功标准")


class OdysseyPath(BaseModel):
    """奥德赛单条人生路径"""
    path_id: str = Field(..., description="路径ID：path_a, path_b, path_c")
    path_name: str = Field(..., description="路径名称")
    path_description: str = Field(..., description="路径描述")
    milestones: List[OdysseyMilestone] = Field(..., description="5年里程碑节点列表")
    risk_level: str = Field(..., description="风险等级：low, medium, high")


class Analysis(BaseModel):
    """🌟 核心可视化分析数据结构"""
    visual_type: VisualType = Field(..., description="可视化类型")
    ikigai_data: Optional[IkigaiData] = Field(None, description="Ikigai雷达图数据")
    barbell_data: Optional[BarbellData] = Field(None, description="杠铃策略模拟器数据")
    odyssey_data: Optional[List[OdysseyPath]] = Field(None, description="奥德赛时间轴数据")
    methodology: Optional[str] = Field(None, description="方法论名称")
    mentor_note: Optional[str] = Field(None, description="导师备注")
    
    @field_validator('ikigai_data')
    @classmethod
    def check_ikigai_data(cls, v, info):
        if info.data['visual_type'] == VisualType.IKIGAI_RADAR and v is None:
            raise ValueError('ikigai_data is required when visual_type is ikigai_radar')
        return v
    
    @field_validator('barbell_data')
    @classmethod
    def check_barbell_data(cls, v, info):
        if info.data['visual_type'] == VisualType.BARBELL_SIMULATOR and v is None:
            raise ValueError('barbell_data is required when visual_type is barbell_simulator')
        return v
    
    @field_validator('odyssey_data')
    @classmethod
    def check_odyssey_data(cls, v, info):
        if info.data['visual_type'] == VisualType.ODYSSEY_TIMELINE and v is None:
            raise ValueError('odyssey_data is required when visual_type is odyssey_timeline')
        return v


class ConversationRequest(BaseModel):
    session_id: str = Field(..., description="会话唯一标识符，用于保持上下文连贯性")
    message: str = Field(..., description="用户的文本输入")
    state: State = Field(..., description="当前会话状态（用于多轮对话）")


class ConversationResponse(BaseModel):
    session_id: str = Field(..., description="会话唯一标识符（与输入一致）")
    response: str = Field(..., description="带有强烈导师人设、一针见血的自然语言指导回复")
    state: State = Field(..., description="动态更新的用户画像与所处的 10 个状态机步骤")
    questions: Optional[List[Question]] = Field(None, description="需要用户回答的问题列表")
    analysis: Optional[Analysis] = Field(None, description="🌟 核心亮点：各阶段的高阶可视化数据载荷")


def get_next_step(current_step: Step) -> Step:
    """获取下一步状态"""
    step_order = [
        Step.INITIAL,
        Step.BACKGROUND,
        Step.PASSION_SKILL,
        Step.MARKET_NEED,
        Step.IKIGAI_ANALYSIS,
        Step.ODYSSEY_PROTOTYPES,
        Step.BARBELL_STRATEGY,
        Step.TRANSITION_PLAN,
        Step.FINAL_SUMMARY,
        Step.COMPLETED
    ]
    current_index = step_order.index(current_step)
    if current_index < len(step_order) - 1:
        return step_order[current_index + 1]
    return Step.COMPLETED


def generate_ikigai_analysis(collected_data: Dict[str, Any]) -> Analysis:
    """生成 Ikigai 雷达图分析数据"""
    passion_score = 75
    skill_score = 65
    market_score = 55
    reward_score = 60
    ai_risk = 35
    
    return Analysis(
        visual_type=VisualType.IKIGAI_RADAR,
        methodology="Ikigai 甜蜜点分析",
        mentor_note="记住，纯粹为了钱会抑郁，纯粹为了理想会饿死。咱得找个平衡点。",
        ikigai_data=IkigaiData(
            passion_score=passion_score,
            skill_score=skill_score,
            market_score=market_score,
            reward_score=reward_score,
            sweet_spot=["AI 应用开发", "出海数字营销", "技术内容创作"],
            high_risk_areas=["纯文科研究", "传统媒体", "基础财务"],
            ai_replacement_risk=ai_risk
        )
    )


def generate_barbell_analysis(collected_data: Dict[str, Any]) -> Analysis:
    """生成杠铃策略模拟器分析数据"""
    return Analysis(
        visual_type=VisualType.BARBELL_SIMULATOR,
        methodology="塔勒布杠铃策略",
        mentor_note="温水煮青蛙的工作最危险，要么极稳要么极激进！",
        barbell_data=BarbellData(
            left_side=BarbellSide(
                name="防守池",
                description="极度安全的生存底座，80%精力投入",
                risk_score=15,
                base_return=15000,
                allocation_percent=80,
                examples=["现有稳定主业", "考公考编", "硬技能兼职"]
            ),
            right_side=BarbellSide(
                name="进攻池",
                description="高爆发力的时代红利，20%精力投入",
                risk_score=85,
                base_return=5000,
                allocation_percent=20,
                examples=["AI 垂直应用", "出海变现", "个人 IP 打造"]
            ),
            total_risk_score=45,
            mentor_note="80%守，20%攻，永远保留翻身的筹码！"
        )
    )


def generate_odyssey_analysis(collected_data: Dict[str, Any]) -> Analysis:
    """生成奥德赛时间轴分析数据"""
    path_a = OdysseyPath(
        path_id="path_a",
        path_name="稳健搞钱流",
        path_description="稳扎稳打，先求生存再谋发展，适合家庭条件一般的朋友",
        risk_level="low",
        milestones=[
            OdysseyMilestone(
                time_point="3months",
                title="稳住基本盘",
                description="把手头工作做好，同时开始小额副业试水",
                actions=["每天高效完成本职工作", "用 AI 工具做简单的海外众包任务"],
                success_criteria="本职不丢，副业月入 2000+"
            ),
            OdysseyMilestone(
                time_point="6months",
                title="副业稳定",
                description="选定一个副业方向，做到稳定收入",
                actions=["深耕一个垂直领域", "建立稳定的客户/流量来源"],
                success_criteria="副业月入 5000+"
            ),
            OdysseyMilestone(
                time_point="1year",
                title="双轨并行",
                description="主业和副业形成互补，抗风险能力显著提升",
                actions=["建立个人作品集", "拓展高质量人脉圈"],
                success_criteria="被动收入覆盖基本生活开支"
            ),
            OdysseyMilestone(
                time_point="3years",
                title="财务安全垫",
                description="积累足够的资金安全垫，可以考虑更大的动作",
                actions=["优化资产配置", "寻找新的增长点"],
                success_criteria="积蓄覆盖 2 年以上生活费"
            ),
            OdysseyMilestone(
                time_point="5years",
                title="选择性自由",
                description="有资本选择自己真正想做的事情",
                actions=["盘点所有资源", "规划下一阶段人生"],
                success_criteria="拥有随时裸辞的底气"
            )
        ]
    )
    
    path_b = OdysseyPath(
        path_id="path_b",
        path_name="红利爆发流",
        path_description="All in 时代红利，高风险高收益，适合年轻、输得起的朋友",
        risk_level="high",
        milestones=[
            OdysseyMilestone(
                time_point="3months",
                title="快速试错",
                description="同时测试 3-5 个方向，找到有正反馈的那个",
                actions=["做 MVP 验证", "研究成功案例", "小步快跑迭代"],
                success_criteria="找到 1 个有正反馈的方向"
            ),
            OdysseyMilestone(
                time_point="6months",
                title="All in 单点",
                description="集中所有资源在一个有正反馈的方向",
                actions=["砍掉其他方向", "深度聚焦单点突破"],
                success_criteria="月收入开始有爆发迹象"
            ),
            OdysseyMilestone(
                time_point="1year",
                title="扩大战果",
                description="验证过的模式快速复制放大",
                actions=["招人/找合伙人", "建立标准化流程", "拓展新渠道"],
                success_criteria="月收入稳定 5 万+"
            ),
            OdysseyMilestone(
                time_point="3years",
                title="建立壁垒",
                description="形成自己的核心竞争力和护城河",
                actions=["建立私域流量池", "打造个人品牌", "沉淀方法论"],
                success_criteria="有稳定的被动收入来源"
            ),
            OdysseyMilestone(
                time_point="5years",
                title="财富自由起点",
                description="建立多元化收入结构，具备抗周期能力",
                actions=["投资布局", "寻找下一代红利", "享受生活"],
                success_criteria="睡后收入覆盖理想生活方式"
            )
        ]
    )
    
    path_c = OdysseyPath(
        path_id="path_c",
        path_name="折中理想流",
        path_description="在现实和理想之间找到平衡，既不委屈自己，也不饿死",
        risk_level="medium",
        milestones=[
            OdysseyMilestone(
                time_point="3months",
                title="理想商业化",
                description="把自己热爱的事情商业化包装",
                actions=["找到理想的付费场景", "设计最小可行性产品", "找到第一批种子用户"],
                success_criteria="理想能赚到第一笔钱"
            ),
            OdysseyMilestone(
                time_point="6months",
                title="验证商业模式",
                description="小范围验证，看理想能否持续赚钱",
                actions=["持续优化产品", "收集用户反馈", "调整商业策略"],
                success_criteria="月收入能稳定覆盖成本"
            ),
            OdysseyMilestone(
                time_point="1year",
                title="平衡发展",
                description="理想和现实形成良性循环",
                actions=["建立稳定的用户群", "打磨产品/服务", "开始少量付费推广"],
                success_criteria="理想相关收入达到主业的 30%"
            ),
            OdysseyMilestone(
                time_point="3years",
                title="理想为主",
                description="理想相关收入超过主业，可以考虑转型",
                actions=["把更多精力转向理想事业", "建立团队扩大规模", "建立品牌影响力"],
                success_criteria="理想事业收入稳定，准备好全职"
            ),
            OdysseyMilestone(
                time_point="5years",
                title="自我实现",
                description="既能做自己热爱的事，又能赚到满意的钱",
                actions=["扩大影响力", "帮助更多人", "享受做这件事的过程"],
                success_criteria="每天醒来都期待去工作"
            )
        ]
    )
    
    return Analysis(
        visual_type=VisualType.ODYSSEY_TIMELINE,
        methodology="《设计人生》奥德赛计划",
        mentor_note="人生不止一种活法，多留几条后路总是好的。",
        odyssey_data=[path_a, path_b, path_c]
    )


def generate_empty_analysis() -> Analysis:
    """生成空分析数据"""
    return Analysis(
        visual_type=VisualType.NONE
    )


def generate_mentor_feedback(current_step: Step, user_message: str) -> str:
    """根据当前步骤和用户输入，生成导师式的点评（先点评，再引导）"""
    if current_step == Step.INITIAL:
        return prompts.INITIAL_WELCOME
    
    elif current_step == Step.BACKGROUND:
        feedback = prompts.generate_background_feedback(user_message)
        return f"{feedback}\n\n{prompts.PASSION_SKILL_PROMPT}"
    
    elif current_step == Step.PASSION_SKILL:
        return f"有意思，这些信息很重要。现在该给你浇点冷水了——让我们看看市场的真实情况。\n\n{prompts.MARKET_NEED_PROMPT}"
    
    elif current_step == Step.MARKET_NEED:
        feedback = prompts.generate_market_feedback(user_message)
        return f"{feedback}\n\n不过别灰心，现实虽然骨感，但咱得找个平衡点。{prompts.IKIGAI_ANALYSIS_PROMPT}"
    
    elif current_step == Step.IKIGAI_ANALYSIS:
        return f"好，甜蜜点咱也找到了。但人生不能只选一条路，我给你设计 3 条完全不同的 5 年路径。{prompts.ODYSSEY_PROTOTYPES_PROMPT}"
    
    elif current_step == Step.ODYSSEY_PROTOTYPES:
        feedback = prompts.generate_barbell_feedback()
        return f"{feedback}\n\n{prompts.BARBELL_STRATEGY_PROMPT}"
    
    elif current_step == Step.BARBELL_STRATEGY:
        feedback = prompts.generate_transition_feedback()
        return f"{feedback}\n\n{prompts.TRANSITION_PLAN_PROMPT}"
    
    elif current_step == Step.TRANSITION_PLAN:
        return f"好了，战略都定了。现在给你一份完整的行动蓝图。{prompts.FINAL_SUMMARY_PROMPT}"
    
    elif current_step == Step.FINAL_SUMMARY:
        return prompts.COMPLETED_PROMPT
    
    else:
        return prompts.COMPLETED_PROMPT


def process_step_transition(request: ConversationRequest) -> ConversationResponse:
    """处理状态转换并生成响应（导师流：先点评，再追问，再前进）"""
    current_step = request.state.current_step
    user_message = request.message
    
    mentor_response = generate_mentor_feedback(current_step, user_message)
    
    updated_state = request.state.model_copy()
    
    if current_step != Step.INITIAL:
        updated_state.collected_data[current_step.value] = user_message
    
    if current_step != Step.INITIAL:
        updated_state.current_step = get_next_step(current_step)
    else:
        updated_state.current_step = Step.BACKGROUND
    
    questions = []
    if updated_state.current_step != Step.COMPLETED:
        raw_questions = prompts.get_step_questions(updated_state.current_step)
        for q in raw_questions:
            questions.append(Question(**q))
    
    analysis = None
    if current_step == Step.IKIGAI_ANALYSIS:
        analysis = generate_ikigai_analysis(updated_state.collected_data)
    elif current_step == Step.BARBELL_STRATEGY:
        analysis = generate_barbell_analysis(updated_state.collected_data)
    elif current_step == Step.ODYSSEY_PROTOTYPES:
        analysis = generate_odyssey_analysis(updated_state.collected_data)
    else:
        analysis = generate_empty_analysis()
    
    return ConversationResponse(
        session_id=request.session_id,
        response=mentor_response,
        state=updated_state,
        questions=questions if questions else None,
        analysis=analysis
    )


@app.post("/webhook", response_model=ConversationResponse)
async def webhook(request: ConversationRequest):
    """
    人生战略级导师智能体 Webhook 接口
    
    具备导师人设的多轮对话引擎：先点评用户回答，再追问，再前进
    🌟 支持三大可视化数据契约：Ikigai 雷达图、杠铃策略沙盘、奥德赛时间轴
    """
    try:
        return process_step_transition(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """健康检查接口"""
    return {"status": "healthy", "service": "career-life-strategist", "version": "3.0.0", "visualization": "enabled"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
