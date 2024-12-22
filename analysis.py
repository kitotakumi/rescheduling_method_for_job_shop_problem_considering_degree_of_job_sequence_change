"""
グラフを描画する関数を格納するモジュール
def plot_scatter:評価関数と世代の散布図
def plot_gantt:ガントチャート
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# 評価関数と世代の散布図
def plot_scatter(ngen, pop_size, all_fitnesses):
    plt.figure(figsize=(10, 5))
    all_generations = []
    # 全個体の世代をall_generationsに格納
    for gen in range(ngen):
        all_generations.append([gen for ind in range(pop_size)])
    # concatenateで[[]]を一次元配列に変換
    plt.scatter(
        np.concatenate(all_generations), np.concatenate(all_fitnesses), alpha=0.5
    )
    plt.title("Evaluation Value per Generation")
    plt.xlabel("generation")
    plt.ylabel("makespan")
    plt.show()


# ガントチャートの表示
def plot_gantt(gannt, num_jobs, num_machines, jsp, reschedule_time=None):
    # ジョブに対応する色のリスト（ジョブの数に応じて動的に生成）
    colors = plt.cm.tab10(range(num_jobs))

    # プロットの作成
    fig, gnt = plt.subplots(figsize=(10, 5))
    gnt.set_ylim(0, num_machines)
    max_time = max(task[1] for machine in gannt for task in machine)
    # gnt.set_xlim(0, max_time)
    gnt.set_xlim(0, 1100)
    gnt.set_xlabel("Time")
    gnt.set_ylabel("Machines")

    # makespanを表示
    gnt.annotate(
        f"Makespan: {max_time}",
        xy=(max_time, 0),
        xytext=(max_time, 0.5),
        arrowprops=dict(facecolor="red", shrink=0.05),
    )

    # マシンごとのY軸ラベル
    gnt.set_yticks([i + 0.5 for i in range(num_machines)])
    gnt.set_yticklabels(["Machine {}".format(i) for i in range(num_machines)])
    gnt.grid(True)

    # ジョブごとにプロット
    for machine, tasks in enumerate(gannt):
        for task in tasks:
            start, end, job = task
            gnt.broken_barh(
                [(start, end - start)], (machine, 1), facecolors=(colors[job])
            )

    # reschedule_time地点で補助線を追加
    if reschedule_time is not None:
        gnt.axvline(x=reschedule_time, color="red", linestyle="--", linewidth=2)
        gnt.annotate(
            f"Reschedule Time: {reschedule_time}",
            xy=(reschedule_time, 0),
            xytext=(reschedule_time, 0.1),
        )

        # arrowprops=dict(facecolor='red', shrink=0.05))

    # 凡例の作成
    patches = [
        mpatches.Patch(color=colors[i], label="Job {}".format(i))
        for i in range(num_jobs)
    ]
    plt.legend(handles=patches, bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.title(f"Gantt Chart for {jsp} Job Shop Scheduling")
    fig.tight_layout()
    plt.show()
