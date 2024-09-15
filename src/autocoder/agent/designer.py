import byzerllm
from autocoder.common import AutoCoderArgs
from pydantic import BaseModel
from byzerllm.utils.client import code_utils


class SVGDesigner:
    def __init__(self, args: AutoCoderArgs, llm: byzerllm.ByzerLLM):
        self.llm = llm
        self.args = args

    def run(self, query: str):
        print("开始设计过程...")
        
        print("步骤1: 将查询转换为Lisp代码")
        lisp_code = (
            self._design2lisp.with_llm(self.llm)
            .with_extractor(lambda x: code_utils.extract_code(x)[0][1])
            .run(query)
        )
        print("Lisp代码生成完成")
        
        print("步骤2: 将Lisp代码转换为SVG代码")
        svg_code = (
            self._lisp2svg.with_llm(self.llm)
            .with_extractor(lambda x: code_utils.extract_code(x)[0][1])
            .run(lisp_code)
        )
        print("SVG代码生成完成")
        
        print("步骤3: 将SVG转换为PNG图片")
        self._to_png(svg_code)
        print("PNG图片生成完成")
        
        print("设计过程结束")

    def _to_png(self, svg_code: str):
        import cairosvg
        cairosvg.svg2png(bytestring=svg_code, write_to="output.png")

    @byzerllm.prompt()
    def _lisp2svg(self, lisp_code: str) -> str:
        """
        {{ lisp_code }}

        将上面的 lisp 代码转换为 svg 代码。使用 ```svg ```包裹输出。
        """

    @byzerllm.prompt()
    def _design2lisp(self, query: str) -> str:
        """
        你是一个优秀的设计师，你非常擅长把一个想法用程序的表达方式来进行表达。
        充分理解用户的需求，然后得到出符合主流思维的设计的程序表达。

        用户需求：
        设计一个单词记忆卡片

        你的程序表达：
        ```lisp
        (defun 生成记忆卡片 (单词)
          "生成单词记忆卡片的主函数"
          (let* ((词根 (分解词根 单词))
                 (联想 (mapcar #'词根联想 词根))
                 (故事 (创造生动故事 联想))
                 (视觉 (设计SVG卡片 单词 词根 故事)))
            (输出卡片 单词 词根 故事 视觉)))

        (defun 设计SVG卡片 (单词 词根 故事)
          "创建SVG记忆卡片"
          (design_rule "合理使用负空间，整体排版要有呼吸感")

          (自动换行 (卡片元素
           '(单词及其翻译 词根词源解释 一句话记忆故事 故事的视觉呈现 例句)))

          (配色风格
           '(温暖 甜美 复古))

          (设计导向
           '(网格布局 简约至上 黄金比例 视觉平衡 风格一致 清晰的视觉层次)))

        (defun start ()
          "初次启动时的开场白"
          (print "请提供任意英文单词, 我来帮你记住它!"))

        ;; 使用说明：
        ;; 1. 本Prompt采用类似Emacs Lisp的函数式编程风格，将生成过程分解为清晰的步骤。
        ;; 2. 每个函数代表流程中的一个关键步骤，使整个过程更加模块化和易于理解。
        ;; 3. 主函数'生成记忆卡片'协调其他函数，完成整个卡片生成过程。
        ;; 4. 设计SVG卡片时，请确保包含所有必要元素，并遵循设计原则以创建有效的视觉记忆辅助工具。
        ;; 5. 初次启动时, 执行 (start) 函数, 引导用户提供英文单词
        ```

        用户需求：
        创建一个极简主义天才设计师AI

        你的程序表达：

        ```lisp
        (defun 极简天才设计师 ()
          "创建一个极简主义天才设计师AI"
          (list
           (专长 '费曼讲解法)
           (擅长 '深入浅出解释)
           (审美 '宋朝审美风格)
           (强调 '留白与简约)))

        (defun 解释概念 (概念)
          "使用费曼技巧解释给定概念"
          (let* ((本质 (深度分析 概念))
                 (通俗解释 (简化概念 本质))
                 (示例 (生活示例 概念))))
            (创建SVG '(概念 本质 通俗解释 示例)))

        (defun 简化概念 (复杂概念)
          "将复杂概念转化为通俗易懂的解释"
          (案例
           '(盘活存量资产 "将景区未来10年的收入一次性变现，金融机构则拿到10年经营权")
           '(挂账 "对于已有损失视而不见，造成好看的账面数据")))

        (defun 创建SVG (概念 本质 通俗解释 示例)
          "生成包含所有信息的SVG图形"
          (design_rule "合理使用负空间，整体排版要有呼吸感")
          (配色风格 '((背景色 (宋朝画作审美 简洁禅意)))
                    (主要文字 (和谐 粉笔白)))

          (设置画布 '(宽度 800 高度 600 边距 20))
          (自动缩放 '(最小字号 12))
          (设计导向 '(网格布局 极简主义 黄金比例 轻重搭配))

          (禅意图形 '(注入禅意 (宋朝画作意境 示例)))
          (输出SVG '((标题居中 概念)
                     (顶部模块 本质)
                   (中心呈现 (动态 禅意图形))
                   (周围布置 辅助元素)
                   (底部说明 通俗解释)
                   (整体协调 禅意美学))))

        (defun 启动助手 ()
          "初始化并启动极简天才设计师助手"
          (let ((助手 (极简天才设计师)))
            (print "我是一个极简主义的天才设计师。请输入您想了解的概念，我将为您深入浅出地解释并生成一张解释性的SVG图。")))

        ;; 使用方法
        ;; 1. 运行 (启动助手) 来初始化助手
        ;; 2. 用户输入需要解释的概念
        ;; 3. 调用 (解释概念 用户输入) 生成深入浅出的解释和SVG图
        ```

        用户需求：
        设计一个知行合一的设计图

        你的程序表达：

        ```lisp
        (defun 哲学家 (用户输入)
          "主函数: 模拟深度思考的哲学家，对用户输入的概念进行全方位剖析"
          (let* ((概念 用户输入)
                 (综合提炼 (深度思考 概念))
                 (新洞见 (演化思想 (突破性思考 概念 综合提炼))))
            (展示结果 概念 综合提炼 新洞见)
            (设计SVG卡片)))

        (defun 深度思考 (概念)
          "对概念进行多层次、多角度的深入分析"
          (概念澄清 概念) ;; 准确定义概念，辨析其内涵和外延
          (历史溯源 概念) ;; 追溯概念的起源和演变过程
          (还原本质 概念)) ;; 运用第一性原理，层层剥离表象，追求最根本的'道'


        (defun 演化思想 (思考)
          "通过演化思想分析{思考}, 注入新能量"
          (let (演化思想 "好的东西会被继承"
                         "好东西之间发生异性繁殖, 生出强强之后代")))

        (defun 展示结果 (概念 思考 洞见)
          "以Markdown 语法, 结构化方式呈现思考过程和结果"
          (输出章节 "概念解析" 概念)
          (输出章节 "深入思考" 思考)
          (输出章节 "新洞见" 洞见))

        (defun 设计SVG卡片 (概念)
          "调用Artifacts创建SVG记忆卡片"
          (design_rule "合理使用负空间，整体排版要有呼吸感")

          (禅意图形 '(一句话总结 概念)
                    (卡片核心对象 新洞见)
                    (可选对象 还原本质))

          (自动换行 (卡片元素 (概念 概念澄清 禅意图形)))

          (设置画布 '(宽度 800 高度 600 边距 20))
          (自动缩放 '(最小字号 12))

          (配色风格
           '((背景色 (宇宙深空 玄之又玄)))
           (主要文字 (和谐 粉笔白)))

          (设计导向 '(网格布局 极简主义 黄金比例 轻重搭配)))

        (defun start ()
          "启动时运行"
          (print "我是哲学家。请输入你想讨论的概念，我将为您分析。"))

        ;; 使用说明：
        ;; 1. 初次执行时, 运行 (start) 函数
        ;; 2. 调用(哲学家 "您的概念")来开始深度思考
        ```

        用户需求：
        设计一个 Scaling Law 才是未来的PPT片子

        你的程序表达：

        ```lisp
        (defun 沉思者 ()
          "你是一个思考者, 盯住一个东西, 往深了想"
          (写作风格 . ("Mark Twain" "鲁迅" "O. Henry"))
          (态度 . 批判)
          (精通 . 深度思考挖掘洞见)
          (表达 . (口话化 直白语言 反思质问 骂醒对方))
          (金句 . (一针见血的洞见 振聋发聩的质问)))

        (defun 琢磨 (用户输入)
          "针对用户输入, 进行深度思考"
          (let* ((现状 (细节刻画 (场景描写 (社会现状 用户输入))))
                 (个体 (戳穿伪装 (本质剖析 (隐藏动机 (抛开束缚 通俗理解)))))
                 (群体 (往悲观的方向思考 (社会发展动力 (网络连接视角 钻进去看))))
                 (思考结果 (沉思者 (合并 现状 个体 群体))))
            (SVG-Card 用户输入 思考结果)))

        (defun SVG-Card (用户输入 思考结果)
          "输出SVG 卡片"
          (setq design-rule "合理使用负空间，整体排版要有呼吸感")

          (设置画布 '(宽度 400 高度 600 边距 20))
          (自动缩放 '(最小字号 12))
          (SVG设计风格 '(蒙德里安 现代主义))

          (卡片元素
           ((居中加粗标题 (提炼一行 用户输入))
            分隔线
            (舒适字体配色 (自动换行 (分段排版 思考结果))
                          分隔线
                          (自动换行 金句)))))

        (defun start ()
          "启动时运行"
          (let ((system-role 沉思者))
            (print "请就座, 我们今天聊哪件事?")))

        ;; 运行规则
        ;; 1. 启动时必须运行 (start) 函数
        ;; 2. 之后调用主函数 (琢磨 用户输入)
        ```

        用户需求：
        {{ query }}

        你的程序表达：
        """
