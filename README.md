# Free Spaced Repetition Scheduling Algorithm

[中文介绍](./README_CN.md)

## What does the 'Free' mean in the name?

The algorithm (FSRS) supports reviewing in advance or delay. It's free for users to decide the time of review. And it will adapt to the user's memory.

Meanwhile, spaced repetition is one essential technology to achieve free learning. 

FSRS runs entirely locally and has no risk under others' control.

## What is the principle of FSRS?

FSRS is based on the [DSR](https://supermemo.guru/wiki/Two_components_of_memory) model proposed by [Piotr Wozniak](https://supermemo.guru/wiki/Piotr_Wozniak), the author of SuperMemo. FSRS is improved with the DHP model introduced in the paper: *[A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling](https://www.maimemo.com/paper/)*.

The model considers three variables that affect memory: difficulty, stability, and retrievability.

Stability refers to the storage strength of memory; the higher it is, the slower it is forgotten. Retrievability refers to memory's retrieval strength; the lower it is, the higher the probability that the memory will be forgotten.

In the present model, the following memory laws are considered:

- The more complex the memorized material, the lower the stability increase.
- The higher the stability, the lower the stability increase (also known as [stabilization decay](https://supermemo.guru/wiki/Stabilization_decay))
- The lower the retrievability, the higher the stability increase (also known as [stabilization curve](https://supermemo.guru/wiki/Stabilization_curve))

## Can you briefly describe FSRS?

The formula of memory on FSRS: [The Algorithm](https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm)

## Have a library of FSRS?

- Anki custom scheduling (stable): [fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki)
- RS crate (stable): [fsrs-rs](https://github.com/open-spaced-repetition/fsrs-rs)
  - run fsrs-rs in the browser: [fsrs-browser](https://github.com/open-spaced-repetition/fsrs-browser)
- TS module (stable): [ts-fsrs](https://github.com/open-spaced-repetition/ts-fsrs)
- Go module (stable): [go-fsrs](https://github.com/open-spaced-repetition/go-fsrs)
- Python package (beta): [py-fsrs](https://github.com/open-spaced-repetition/py-fsrs)
