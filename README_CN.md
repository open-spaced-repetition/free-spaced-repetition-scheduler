# 自由间隔重复调度算法

[Introduction in English](./README.md)

## 名称中的「自由」是什么意思？

FSRS 支持自由复习，可以提前，也可以推迟，算法会根据记忆模型进行适应。

同时，间隔重复是实现自由学习的基础技术之一。

FSRS 可以在本地运行，无需担心泄露自己的学习数据。

## 算法的原理是什么？

本算法基于 SuperMemo 作者 [Piotr Wozniak](https://supermemo.guru/wiki/Piotr_Wozniak) 提出的 [DSR 模型](https://supermemo.guru/wiki/Two_components_of_memory)开发。FSRS 在此基础上，根据论文 *[A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling](https://www.maimemo.com/paper/)* 中的 DHP 模型进行改进。

该模型考虑了影响记忆的三个变量：难度（difficulty），稳定性（stability）和可提取性（retrievability）。

稳定性指的是记忆的存储强度，越高，记忆遗忘得越慢。可提取性指的是记忆的检索强度，越低，记忆遗忘的概率越高。

在本模型中，考虑了以下记忆规律：

- 记忆材料越难，记忆稳定性增长越慢
- 记忆稳定性越高，记忆稳定性增长越慢（又称为[记忆稳定化衰减](https://supermemo.guru/wiki/Stabilization_decay)）
- 记忆可提取性越低，记忆稳定性增长越快（又称为[记忆稳定化曲线](https://supermemo.guru/wiki/Stabilization_curve)）

## 能简单描述一下算法吗？

FSRS 的记忆公式: [Free Spaced Repetition Scheduler](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)

## 有现成的算法库吗？

- 调度器:
  - TypeScipt module: [ts-fsrs](https://github.com/open-spaced-repetition/ts-fsrs)
  - Golang module: [go-fsrs](https://github.com/open-spaced-repetition/go-fsrs)
  - Python package: [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs)
  - Rust crate: [rs-fsrs](https://github.com/open-spaced-repetition/rs-fsrs)
  - Clojure library: [cljc-fsrs](https://github.com/open-spaced-repetition/cljc-fsrs)
  - Dart package: [dart-fsrs](https://github.com/open-spaced-repetition/dart-fsrs)
  - Ruby gem: [rb-fsrs](https://github.com/open-spaced-repetition/rb-fsrs)
  - Swift package: [swift-fsrs](https://github.com/open-spaced-repetition/swift-fsrs)
  - Android library: [android-fsrs](https://github.com/open-spaced-repetition/android-fsrs)
  - Exlixir library: [ex_fsrs](https://github.com/open-spaced-repetition/ex_fsrs)

- 优化器:
  - Python package (stable): [fsrs-optimizer](https://github.com/open-spaced-repetition/fsrs-optimizer)
  - RS crate (stable): [fsrs-rs](https://github.com/open-spaced-repetition/fsrs-rs)
    - run fsrs-rs in the browser: [fsrs-browser](https://github.com/open-spaced-repetition/fsrs-browser)
