# 自由间隔重复调度算法

[Introduction in English](./README.md)

## 名称中的「自由」是什么意思？

本算法支持自由复习，可以提前，也可以推迟，算法会根据记忆模型进行适应。

同时，间隔重复是实现自由学习的基础技术之一。而且算法可以在本地运行，无需担心泄露自己的学习数据。

## 算法的原理是什么？

本算法基于 SuperMemo 作者 [Piotr Wozniak](https://supermemo.guru/wiki/Piotr_Wozniak) 提出的 [DSR 模型](https://supermemo.guru/wiki/Two_components_of_memory)开发。FSRS 在此基础上，根据论文 *[A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling](https://dl.acm.org/doi/10.1145/3534678.3539081)* 中的 DHP 模型进行改进。

该模型考虑了影响记忆的三个变量：难度（difficulty），稳定性（stability）和可提取性（retrievability）。

稳定性指的是记忆的存储强度，越高，记忆遗忘得越慢。可提取性指的是记忆的检索强度，越低，记忆遗忘的概率越高。

在本模型中，考虑了以下记忆规律：

- 记忆材料越难，记忆稳定性增长越慢
- 记忆稳定性越高，记忆稳定性增长越慢（又称为[记忆稳定化衰减](https://supermemo.guru/wiki/Stabilization_decay)）
- 记忆可提取性越低，记忆稳定性增长越快（又称为[记忆稳定化曲线](https://supermemo.guru/wiki/Stabilization_curve)）

## 能简单描述一下算法吗？

- 难度范围 $D\in [1,10]$
- 初始难度 $D_0 = 5$
- 初始稳定性 $S_0 = 2$
- 指数遗忘曲线模型 $R = \exp(\ln 0.9 \cdot \cfrac{I}{S})$
- 复习成功后稳定性更新公式 $S^\prime=S\cdot (1 + a \times D ^ {-b} \times S^{-c} \times (\exp(1 - R)-1))$
    - 稳定性增长系数 a = 60
    - 难度衰减系数 b = 0.7
    - 稳定性衰减系数 c = 0.2
- 复习失败后的稳定性 $S_{L} = S_0^{-f\cdot L}$
    - 遗忘次数 $L >= 0$
    - 遗忘衰减系数 f = 0.3
- 复习后难度更新公式 $D^\prime = D - d\cdot(Grade - 1) - e\cdot(1-R)$
    - 评分范围 $Grade\in \{0,1,2\}$
        - 0 表示遗忘（复习失败）
        - 1 表示记住（复习成功）
        - 2 表示容易（复习成功）
    - 评分影响系数 d = 1
    - 可提取性影响系数 e = 1
- 初始稳定性自适应 $S_0 = \cfrac{\ln 0.9}{\cfrac{\sum\limits_i^n \ln R_i \times I_i\times cnt_i}{\sum\limits_i^n I_i^2\times
  cnt_i}}$
    - 即对第一次复习到遗忘曲线进行线性回归，计算实际的稳定性
- 初始难度自适应 $D_0 = \cfrac{\ln R_t}{\ln R_c}^{\frac{1}{-b}} \times D_0$
    - 目标保留率 $R_t$
    - 目前保留率 $R_c$
    - 如果 $R_c < R_t$ ，就提高初始难度，这样新卡片的复习间隔增长速度就会下降，反之亦然

## 有现成的算法库吗？

太微的钓鱼插件实现了该算法的 JavaScript 版本：[fsrs.js](https://github.com/open-spaced-repetition/fsrs.js)，本项目中的 simulator.py 中实现了 Python 版本。Go 版本在 [go-fsrs](https://github.com/open-spaced-repetition/go-fsrs)。为 Anki 特制的简化版在 [fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki)。

该算法尚未稳定，还有待收集数据验证。很多参数是人工设置的，尚未实现自适应，所以目前没有提供算法库。

## 我可以使用该算法吗？

可以，但请在项目中指向本仓库。
