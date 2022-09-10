# Free Spaced Repetition Scheduling Algorithm

[中文介绍](./README_CN.md)

## What does the 'Free' mean in the name?

The algorithm (FSRS) supports reviewing in advance or delay. It's free for users to decide the time of review. And it will adapt to the user's memory.

Meanwhile, spaced repetition is one essential technology to achieve free learning. 

FSRS runs entirely locally and has no risk under others' control.

## What is the principle of FSRS?

FSRS is based on the [DSR](https://supermemo.guru/wiki/Two_components_of_memory) model proposed by [Piotr Wozniak](https://supermemo.guru/wiki/Piotr_Wozniak), the author of SuperMemo. FSRS is improved with the DHP model introduced in the paper: *[A Stochastic Shortest Path Algorithm for Optimizing Spaced Repetition Scheduling](https://dl.acm.org/doi/10.1145/3534678.3539081)*.

The model considers three variables that affect memory: difficulty, stability, and retrievability.

Stability refers to the storage strength of memory; the higher it is, the slower it is forgotten. Retrievability refers to memory's retrieval strength; the lower it is, the higher the probability that the memory will be forgotten.

In the present model, the following memory laws are considered:

- The more complex the memorized material, the lower the stability increase.
- The higher the stability, the lower the stability increase (also known as [stabilization decay](https://supermemo.guru/wiki/Stabilization_decay))
- The lower the retrievability, the higher the stability increase (also known as [stabilization curve](https://supermemo.guru/wiki/Stabilization_curve))

## Can you briefly describe FSRS?

- Difficulty range - $D\in [1,10]$
- Initial difficulty - $D_0 = 5$
- Initial stability - $S_0 = 2$
- Exponential forgetting curve model - $R = \exp(\ln 0.9 \cdot \cfrac{I}{S})$
- Stability updating formula after successful review - $S^\prime = S\cdot (1 + a \times D ^ {-b} \times S^{-c} \times (\exp(1 - R)-1))$
  - Stability increase coefficient - a = 60
  - Difficulty decay coefficient - b = 0.7
  - Stability decay coefficient - c = 0.2
- Stability after failed review - $S_{L} = S_0^{-f\cdot L}$
  - Number of lapses - $L >= 0$
  - Forgetting decay coefficient - f = 0.3
- Difficulty updating formula after review - $D^\prime = D - d\cdot(Grade - 1) - e\cdot(1-R)$
  - Rating range - $Grade\in \{0,1,2\}$
    - 0 means forgetting (failed review)
    - 1 indicates remembered (successful review)
    - 2 indicates so easy (successful review without effort)
  - Grading influence coefficient - d = 1
  - Retrievability influence coefficient - e = 1
- Adaptive initial stability  - $S_0 = \cfrac{\ln 0.9}{\cfrac{\sum_i^n \ln R_i \times I_i\times cnt_i}{\sum\limits_i^n I_i^2\times cnt_i}}$
    - A linear regression of the first review to the forgetting curve is performed to calculate the actual stability.
- Adaptive initial difficulty $D_0 = \cfrac{\ln R_t}{\ln R_c}^{\frac{1}{-b}} \times D_0$
  - Requested recall rate - $R_t$
  - Current recall rate - $R_c$
  - If $R_c < R_t$, increase the initial difficulty so that the growth rate of the review interval for new cards decreases, and vice versa

## Have a library of FSRS?

The fishing plugin of tiddlywiki implements a JavaScript version of FSRS: [fsrs.js](https://github.com/open-spaced-repetition/fsrs.js) and the Python version is implemented in simulator.py in this repository. The Go version is at [go-fsrs](https://github.com/open-spaced-repetition/go-fsrs). And the simplified version for Anki is at [fsrs4anki](https://github.com/open-spaced-repetition/fsrs4anki).

FSRS is not yet stable and has yet to be verified by collecting data. Many parameters are set manually and are not yet adaptable, so there is no library available for FSRS in other programming languages.

## Can I use FSRS in my software?

Yes, please link to this [repository](https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler).
