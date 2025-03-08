# ジョブショップスケジューリング問題におけるジョブの投入順序の変更量を考慮した再スケジューリング手法の提案
- 本リポジトリは、ジョブショップスケジューリング問題に対する初期スケジューリングおよび外乱発生時の再スケジューリングを、遺伝的アルゴリズム（GA）を用いて解決するための各種関数群およびクラスを実装しているものである。本研究はスケジュールの効率性（総所要時間）とスケジュールの安定性（ジョブの投入順序の変更量に基づく指標）を目的関数として評価し、二目的最適化を行う点に特徴がある。
- 本研究では谷水義隆教授の論文および早稲田大学谷水研究室で用いられているコードと[こちらの記事](https://qiita.com/YosukeKentuckyFriedChicken/items/80d1cb70d96bd4586f59)を主に参考にしている。
## 研究概要
製造現場では、作業遅延、機械故障などの予期せぬ外乱が発生し、生産性の低下、コスト増大といった企業競争力への悪影響をもたらす。外乱に対応するアプローチとしてリアクティブスケジューリングは有効な手法であるが、頻繁な再スケジューリングにより現場の混乱やリソース再配置、原材料再注文などのコストが増加する。<br/>
本研究は、スケジュール変更コストを抑制するため、元のスケジュールからの変更度合い、特にジョブの投入順序の変更に着目した安定性を確保する再スケジューリング手法を提案する。ジョブの投入順序を順位として評価し、順位の変更量に着目した順位偏差という関数を定義する。さらに、再スケジューリング時刻からの順位的距離に応じたペナルティ関数を設定することで、各ジョブのスケジュール変更コストの変化量を表現する。<br/>
GAの目的関数に総所要時間と安定性関数を組み込み、重みパラメータ法により二目的最適化を行った結果、10ジョブ10リソースのジョブショップスケジューリング問題において、総所要時間をほとんど悪化させずに安定性関数値を大幅に抑制できること、および定義した安定性が確保された再スケジューリングが実現されることを確認した。

## コード概要
- **src/job_shop_scheduling.py**
  - ジョブショップスケジューリング問題の各種データ構造およびクラスを定義している。
  - 基底クラス JobMachineTableBase により、各問題ごとの機械番号や加工時間のテーブル、初期ガントチャート、遅延ガントチャートの取得メソッドが提供される。
  - また、遺伝子をガントチャートに展開する際に利用する補助クラス JobMachineChild およびリスケジューリング時に利用する JobMachineChild_Reactive が定義され、各ジョブの次工程の開始時刻や処理時間の管理を行う。
  - 具体例として、MT6_6 および MT10_10 という2種類のジョブショップ問題がクラスとして実装され、各問題に対応するデータが格納されている。
- **src/gantt_chart_operation.py**
  - ガントチャートの生成および操作に関する関数群を格納している。
  - 遺伝子表現からガントチャートへ展開する get_gantt、および外乱発生後のリスケジューリング用ガントチャートを生成する get_gantt_reactive が含まれる。
  - ガントチャートの1次元・2次元変換や、作業の遅延を検出する check_disturbance、さらにリスケジューリング後のガントチャートを構築する create_rsr_gantt も提供している。
  - 最後に、リスケ対象作業を遺伝子表現へ変換する get_gene 関数が定義され、GAとの連携を図っている。
- **src/genetic_operaton.py**
  - GAにおける各種遺伝子操作（初期個体生成、交叉、突然変異、選択）および評価関数の定義を行っているモジュールである。
  - 初期スケジューリング用およびリスケジューリング用の個体生成関数（create_individual、create_individual_reactive）が実装されている。
  - 交叉では PMX および JSP向けの2点交叉（crossover_pmx、crossover_hirano）が、突然変異では逆位（mutation_inversion）および JSP用の突然変異（mutation_hirano）が提供されている。
  - また、評価関数としてメイクスパンの逆数を算出する makespan や、リアクティブスケジューリングにおける評価関数 makespan_reactive、makespan_reactive2 が定義されている。
  - さらに、ジョブの投入順序の変更量を評価するための「順位偏差」や、これに順位的距離を掛け合わせた安定性関数（stability_function_v3、stability_function_stat）が実装され、重みパラメータ法に基づいた目的関数（objective_function_v3）に統合されている。
  - 遺伝的アルゴリズムの初期化や、個体群の評価値の最大・最小値を取得する get_max_min、および開始時刻の偏差を評価する関数も含まれている。
- **src/main_initial_scheduling.py**
  - 初期スケジューリングの実行を目的とするメインプログラムである。
  - パラメータ設定、GAによる世代更新、個体の評価、最良個体の選出を行い、最終的に散布図およびガントチャートを描画して結果を可視化する。
  - ここでは、初期スケジュールの最適化を通して、総所要時間（メイクスパン）の最小化が主な目的となる。
- **src/main_stability_scheduling.py**
  - 外乱発生時のリアクティブスケジューリングを実行するメインプログラムである。
  - 初期スケジュールおよび遅延が発生したガントチャートから、固定（変更不要）な作業とリスケジューリング対象の作業を判別する。
  - スケジューリング対象作業を遺伝子表現に変換し、GAによる二目的最適化（メイクスパンと安定性のバランス）の手法を実装している。
  - 各世代の評価値の記録および最良個体のガントチャートの描画を通して、安定性を考慮した再スケジューリングの効果を検証する。
- **src/analysis.py**
  - 本モジュールは、評価結果や最良個体の解析のためにグラフ描画の関数群を提供している。
  - plot_scatter: 各世代における評価関数の値（メイクスパンの逆数など）を散布図として表示する関数である。
  - plot_gantt: ガントチャートを描画する関数であり、ジョブの開始・終了時刻および機械ごとの作業割当を視覚化する。
- **src/stat2.py**
  - リスケジューリングに関する統計解析を実施するためのスクリプトである。
  - main_stability_scheduling を複数回実行し、各実行結果（メイクスパン、安定性指標、順位偏差など）をCSVファイルに出力する。
  - さらに、収束率や収束回数、非収束回数、統計的な平均値などを計算し、実験結果の傾向を解析することを目的としている。
