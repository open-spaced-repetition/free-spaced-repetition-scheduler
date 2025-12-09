# Free Spaced Repetition Scheduling Algorithm

[中文介绍](./README_CN.md)

## What does the 'Free' mean in the name?

The algorithm (FSRS) supports reviewing in advance or delay. It's free for users to decide the time of review. And it will adapt to the user's memory.

Meanwhile, spaced repetition is one essential technology to achieve free learning. 

FSRS runs entirely locally and has no risk under others' control.

## What is the principle of FSRS?

FSRS springs from [MaiMemo's DHP model](https://www.maimemo.com/paper/) ([中文介绍](https://memodocs.maimemo.com/docs/2022_KDD)), which is a variant of the [DSR model](https://supermemo.guru/wiki/Three_component_model_of_memory) proposed by [Piotr Wozniak](https://supermemo.guru/wiki/Piotr_Wozniak).

The model considers three variables that affect memory: difficulty, stability, and retrievability.

Stability refers to the storage strength of memory; the higher it is, the slower it is forgotten. Retrievability refers to memory's retrieval strength; the lower it is, the higher the probability that the memory will be forgotten.

In the present model, the following memory laws are considered:

- The more complex the memorized material, the lower the stability increase.
- The higher the stability, the lower the stability increase (also known as [stabilization decay](https://supermemo.guru/wiki/Stabilization_decay))
- The lower the retrievability, the higher the stability increase (also known as [stabilization curve](https://supermemo.guru/wiki/Stabilization_curve))

## Can you briefly describe FSRS?

The formula of memory on FSRS: [The Algorithm](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)

## Have a library of FSRS?

- Scheduler:
  - TypeScipt module: [ts-fsrs](https://github.com/open-spaced-repetition/ts-fsrs)
  - Golang module: [go-fsrs](https://github.com/open-spaced-repetition/go-fsrs)
  - Python package: [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs)
  - Rust crate: [rs-fsrs](https://github.com/open-spaced-repetition/rs-fsrs)
  - Clojure library: [cljc-fsrs](https://github.com/open-spaced-repetition/cljc-fsrs)
  - Dart package: [dart-fsrs](https://github.com/open-spaced-repetition/dart-fsrs)
  - Ruby gem: [rb-fsrs](https://github.com/open-spaced-repetition/rb-fsrs)
  - Swift package: [swift-fsrs](https://github.com/open-spaced-repetition/swift-fsrs)
  - Android library: [android-fsrs](https://github.com/open-spaced-repetition/android-fsrs)
  - Elixir library: [ex_fsrs](https://github.com/open-spaced-repetition/ex_fsrs)

- Optimizer:
  - Python package (stable): [fsrs-optimizer](https://github.com/open-spaced-repetition/fsrs-optimizer)
  - RS crate (stable): [fsrs-rs](https://github.com/open-spaced-repetition/fsrs-rs)
    - run fsrs-rs in the browser: [fsrs-browser](https://github.com/open-spaced-repetition/fsrs-browser)
