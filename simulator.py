import numpy as np
import pandas as pd
import random
from tqdm import tqdm
import matplotlib.pyplot as plt

plt.style.use('seaborn-whitegrid')
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

theory_difficulty_decay = -0.7
theory_stability_decay = -0.2
theory_increase_factor = 120

pred_difficulty_decay = -0.7
pred_stability_decay = -0.2
pred_increase_factor = 60


def update_stability_t(d, s, r):
    return s * (1 + theory_increase_factor * np.power(d, theory_difficulty_decay) * np.power(s,
                                                                                             theory_stability_decay) * (
                        np.exp(1 - r) - 1))


def update_stability_p(d, s, r):
    return s * (1 + pred_increase_factor * np.power(d, pred_difficulty_decay) * np.power(s, pred_stability_decay) * (
            np.exp(1 - r) - 1))


def difficulty2stability(d):
    return np.log(0.9) / np.log(0.95 + 0.005 * (10 - d))


def cal_stability_p_default(log: pd.DataFrame, s_old):
    ivl_list = []
    recall_list = []
    cnt_list = []
    tmp = log[log['Lapses'] == 0].copy()
    tmp['Recall'] = tmp['Grade'].map(lambda x: 0 if x == 0 else 1)
    if len(tmp) > 0:
        for ivl in set(tmp['Ivl'].values):
            r = tmp[tmp['Ivl'] == ivl]['Recall'].mean()
            if r > 0:
                ivl_list.append(ivl)
                recall_list.append(r)
                cnt_list.append(tmp[tmp['Ivl'] == ivl]['Recall'].count())
        zip_list = zip(ivl_list, recall_list, cnt_list)
        logr_ivl_cnt = sum([np.log(r) * ivl * cnt for ivl, r, cnt in zip_list])
        zip_list = zip(ivl_list, recall_list, cnt_list)
        ivl_ivl_cnt = sum(
            [ivl ** 2 * cnt for ivl, _, cnt in zip_list])
        s_new = max(np.log(0.9) / (logr_ivl_cnt / ivl_ivl_cnt), 0.1)
        return (s_new + s_old) / 2
    else:
        return s_old


if __name__ == "__main__":
    random.seed(114514)
    card_per_day_limit = 100
    learn_limit = 100
    review_limit = 100
    deck_size = 100000  # 新卡片总量
    learn_days = 300
    period_len = 15
    request_recall = 0.9

    D_p_default = 5
    S_p_default = 2

    new_card_per_day = np.array([0.0] * learn_days)
    new_card_per_day_average_per_period = np.array([0.0] * learn_days)
    workload_per_day = np.array([0.0] * learn_days)
    workload_per_day_average_per_period = np.array([0.0] * learn_days)

    feature_list = ['D_t', 'S_t', 'R_t', 'D_p', 'S_p', 'R_p', 'Ivl', 'Due', 'Last', 'Lapses', 'Reps', 'IvlHistory',
                    'GradeHistory']
    card_map = {
        'D_t': 0, 'S_t': 1, 'R_t': 2, 'D_p': 3, 'S_p': 4, 'R_p': 5, 'Ivl': 6, 'Due': 7, 'Last': 8, 'Lapses': 9,
        'Reps': 10, 'IvlHistory': 11, 'GradeHistory': 12
    }
    dtypes = np.dtype([
        ('D_t', int),
        ('S_t', float),
        ('R_t', float),
        ('D_p', float),
        ('S_p', float),
        ('R_p', float),
        ('Ivl', int),
        ('Due', int),
        ('Last', int),
        ('Lapses', int),
        ('Reps', int),
        ('IvlHistory', str),
        ('GradeHistory', str),
    ])

    df_card = pd.DataFrame(np.full(deck_size, np.nan, dtype=dtypes), index=range(deck_size), columns=feature_list)
    df_card['D_t'] = df_card['D_t'].map(lambda x: round(max(min(random.gauss(5.5, 2), 10), 1)))
    df_card['S_t'] = df_card['D_t'].map(difficulty2stability)
    df_card['Due'] = learn_days
    df_card['Reps'] = 0
    df_card['Lapses'] = 0

    feature_list = ['Lapses', 'Ivl', 'Memorized', 'Total']
    dtypes = np.dtype([
        ('Lapses', int),
        ('Ivl', int),
        ('Memorized', int),
        ('Total', int),
    ])

    df_collection = pd.DataFrame(columns=feature_list)

    df_log = pd.DataFrame(columns=['Lapses', 'Ivl', 'Grade'])

    total_case = 0
    total_diff = 0
    total_review = 0

    for day in tqdm(range(learn_days)):
        df_card["Ivl"] = day - df_card["Last"]
        df_card["R_t"] = np.exp(np.log(0.9) * df_card["Ivl"] / df_card["S_t"])
        df_card["R_p"] = np.exp(np.log(0.9) * df_card["Ivl"] / df_card["S_p"])

        need_review = df_card[df_card['Due'] <= day].sort_values(by='R_p')
        true_review = need_review.index[:review_limit]
        reviewed = len(true_review)
        for idx in true_review:
            D_t = df_card.iat[idx, card_map['D_t']]
            R_t = df_card.iat[idx, card_map['R_t']]
            S_t = df_card.iat[idx, card_map['S_t']]
            D_p = df_card.iat[idx, card_map['D_p']]
            R_p = df_card.iat[idx, card_map['R_p']]
            S_p = df_card.iat[idx, card_map['S_p']]
            Ivl = df_card.iat[idx, card_map['Ivl']]
            Reps = df_card.iat[idx, card_map['Reps']]
            Lapses = df_card.iat[idx, card_map['Lapses']]
            Grade = 0
            grade_seed = random.random()
            if grade_seed < R_t:
                if grade_seed < R_t ** 10:
                    Grade = 2
                else:
                    Grade = 1

                if Reps > 1:
                    total_diff += 1 - R_p
                    total_case += 1

                df_card.iat[idx, card_map['D_p']] = min(max(D_p + R_p - Grade + 0.2, 1), 10)
                df_card.iat[idx, card_map['S_t']] = update_stability_t(D_t, S_t, R_t)

                df_card.iat[idx, card_map['S_p']] = update_stability_p(df_card.iat[idx, card_map['D_p']], S_p, R_p)
                df_card.iat[idx, card_map['Reps']] += 1
            else:
                Grade = 0

                if Reps > 1:
                    total_diff += - R_p
                    total_case += 1

                df_card.iat[idx, card_map['D_p']] = min(max(D_p + R_p - Grade + 0.2, 1), 10)
                df_card.iat[idx, card_map['S_t']] = difficulty2stability(D_t)

                df_card.iat[idx, card_map['S_p']] = S_p_default * np.exp(-0.3 * (Lapses + 1))
                df_card.iat[idx, card_map['Lapses']] = Lapses + 1
                df_card.iat[idx, card_map['Reps']] = 1

            df_card.iat[idx, card_map['GradeHistory']] += str(Grade)
            df_card.iat[idx, card_map['IvlHistory']] += f'{Ivl},'
            df_card.iat[idx, card_map['Last']] = day
            df_card.iat[idx, card_map['Due']] = day + round(df_card.iat[idx, card_map['S_p']] * np.log(
                request_recall) / np.log(0.9))

            if Reps == 1:
                df_log = df_log.append({'Lapses': Lapses, 'Ivl': Ivl, 'Grade': Grade}, ignore_index=True)

        S_p_default = cal_stability_p_default(df_log, S_p_default)

        if total_case > 100:
            D_p_default = 1 / np.power(total_review, 0.3) * np.power(
                np.log(request_recall) / np.log(request_recall + total_diff / total_case),
                1 / pred_difficulty_decay) * 5 + (1 - 1 / np.power(total_review, 0.3)) * D_p_default
            total_diff = 0
            total_case = 0

        need_learn = df_card[(df_card['Reps'] == 0) & (df_card['Lapses'] == 0)]
        true_learn = need_learn.index[:min(learn_limit, card_per_day_limit - len(true_review))]
        learned = len(true_learn)
        for idx in true_learn:
            df_card.iat[idx, card_map['D_p']] = D_p_default
            df_card.iat[idx, card_map['S_p']] = S_p_default
            df_card.iat[idx, card_map['Last']] = day
            df_card.iat[idx, card_map['Due']] = day + round(S_p_default * np.log(request_recall) / np.log(0.9))
            df_card.iat[idx, card_map['Reps']] = 1

        new_card_per_day[day] = learned
        workload_per_day[day] = learned + reviewed
        total_review += reviewed

        if day >= period_len:
            new_card_per_day_average_per_period[day] = np.true_divide(new_card_per_day[day - period_len:day].sum(),
                                                                      period_len)
            workload_per_day_average_per_period[day] = np.true_divide(workload_per_day[day - period_len:day].sum(),
                                                                      period_len)
        else:
            new_card_per_day_average_per_period[day] = np.true_divide(new_card_per_day[:day + 1].sum(), day + 1)
            workload_per_day_average_per_period[day] = np.true_divide(workload_per_day[:day + 1].sum(), day + 1)

    total_learned = int(sum(new_card_per_day))
    total_reviewed = int(sum(workload_per_day)) - total_learned

    plt.figure(1)
    plt.plot(new_card_per_day_average_per_period, label=f'learned={total_learned}|recall={request_recall:.2f}')
    plt.ylim((0, card_per_day_limit + 10))

    plt.figure(2)
    plt.plot(workload_per_day_average_per_period, label=f'reviewed={total_reviewed}|recall={request_recall:.2f}')

    plt.figure(1)
    plt.title(f"每日学习上限:{card_per_day_limit}-学习天数{learn_days}")
    plt.xlabel("时间/天")
    plt.ylabel(f"每日新学数量({period_len}天平均)")
    plt.legend()

    plt.figure(2)
    plt.title(f"每日学习上限:{card_per_day_limit}-学习天数{learn_days}")
    plt.xlabel("时间/天")
    plt.ylabel(f"每日学习数量({period_len}天平均)")
    plt.legend()
    plt.show()
