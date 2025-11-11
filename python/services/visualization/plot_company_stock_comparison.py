import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import sys
import os

# パス設定をインポート
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import IMAGE_DIR

# 日本語フォント設定
plt.rcParams['font.sans-serif'] = ['MS Gothic', 'Yu Gothic', 'Hiragino Sans']
plt.rcParams['axes.unicode_minus'] = False

# データ
scenarios = ['Scenario 1\n(Keep 20.66%)', 'Scenario 2\n(Reduce to 15%)',
             'Scenario 3\n(Reduce to 10%)', 'Scenario 4\n(Sell 50%)']
company_stock_ratio = [20.66, 15.00, 10.00, 10.27]
expected_return = [6.51, 6.38, 6.25, 6.26]
portfolio_risk = [19.07, 18.06, 17.26, 17.30]
sharpe_ratio = [0.315, 0.325, 0.333, 0.333]
total_score = [40, 71, 85, 70]
tax_cost = [0, 2.3, 4.4, 4.3]

# カラー設定
colors = ['#ff6b6b', '#ffd93d', '#4ecdc4', '#95e1d3']

# Figure作成
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
fig.suptitle('Company Stock Sale Strategy: Statistical Comparison', fontsize=20, fontweight='bold')

# 1. 個別株比率
ax1 = axes[0, 0]
bars1 = ax1.bar(scenarios, company_stock_ratio, color=colors)
ax1.axhline(y=15, color='orange', linestyle='--', linewidth=2, label='Recommended Max (15%)')
ax1.axhline(y=10, color='green', linestyle='--', linewidth=2, label='Conservative Max (10%)')
ax1.set_ylabel('Company Stock Ratio (%)', fontsize=12)
ax1.set_title('1. Individual Stock Concentration', fontsize=14, fontweight='bold')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)
for i, v in enumerate(company_stock_ratio):
    ax1.text(i, v + 0.5, f'{v:.2f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# 2. ポートフォリオリスク
ax2 = axes[0, 1]
bars2 = ax2.bar(scenarios, portfolio_risk, color=colors)
ax2.set_ylabel('Portfolio Risk (%)', fontsize=12)
ax2.set_title('2. Portfolio Risk (Volatility)', fontsize=14, fontweight='bold')
ax2.grid(axis='y', alpha=0.3)
for i, v in enumerate(portfolio_risk):
    ax2.text(i, v + 0.3, f'{v:.2f}%', ha='center', va='bottom', fontsize=11, fontweight='bold')

# 3. シャープレシオ
ax3 = axes[0, 2]
bars3 = ax3.bar(scenarios, sharpe_ratio, color=colors)
ax3.set_ylabel('Sharpe Ratio', fontsize=12)
ax3.set_title('3. Sharpe Ratio (Risk-Adjusted Return)', fontsize=14, fontweight='bold')
ax3.grid(axis='y', alpha=0.3)
for i, v in enumerate(sharpe_ratio):
    ax3.text(i, v + 0.005, f'{v:.3f}', ha='center', va='bottom', fontsize=11, fontweight='bold')

# 4. 総合スコア
ax4 = axes[1, 0]
bars4 = ax4.bar(scenarios, total_score, color=colors)
ax4.set_ylabel('Total Score', fontsize=12)
ax4.set_title('4. Total Score (0-100)', fontsize=14, fontweight='bold')
ax4.set_ylim([0, 100])
ax4.grid(axis='y', alpha=0.3)
for i, v in enumerate(total_score):
    ax4.text(i, v + 2, f'{v} points', ha='center', va='bottom', fontsize=11, fontweight='bold')

# 5. 税コスト
ax5 = axes[1, 1]
bars5 = ax5.bar(scenarios, tax_cost, color=colors)
ax5.set_ylabel('Tax Cost (10,000 JPY)', fontsize=12)
ax5.set_title('5. Capital Gains Tax', fontsize=14, fontweight='bold')
ax5.grid(axis='y', alpha=0.3)
for i, v in enumerate(tax_cost):
    if v > 0:
        ax5.text(i, v + 0.1, f'{v:.1f}万円', ha='center', va='bottom', fontsize=11, fontweight='bold')
    else:
        ax5.text(i, v + 0.1, 'None', ha='center', va='bottom', fontsize=11, fontweight='bold')

# 6. リスク vs リターン（散布図）
ax6 = axes[1, 2]
scatter = ax6.scatter(portfolio_risk, expected_return, s=[score*10 for score in total_score],
                     c=colors, alpha=0.6, edgecolors='black', linewidth=2)
for i, txt in enumerate(['S1', 'S2', 'S3', 'S4']):
    ax6.annotate(txt, (portfolio_risk[i], expected_return[i]),
                ha='center', va='center', fontsize=12, fontweight='bold')
ax6.set_xlabel('Portfolio Risk (%)', fontsize=12)
ax6.set_ylabel('Expected Return (%)', fontsize=12)
ax6.set_title('6. Risk vs Return (Size = Score)', fontsize=14, fontweight='bold')
ax6.grid(True, alpha=0.3)

# レイアウト調整
plt.tight_layout()

# 保存
plt.savefig(os.path.join(IMAGE_DIR, 'company_stock_comparison.png'), dpi=300, bbox_inches='tight')
print("Chart saved: company_stock_comparison.png")

# 過去の暴落シミュレーション
fig2, ax = plt.subplots(figsize=(14, 8))

crashes = ['2000 IT Bubble\n(-45% ACWI, -70% IT)',
           '2008 Lehman Shock\n(-50% ACWI, -60% IT)',
           '2022 Tech Crash\n(-20% ACWI, -40% IT)']

# 損失額データ（万円）
scenario1_losses = [617, 631, 302]
scenario2_losses = [595, 621, 284]
scenario3_losses = [575, 613, 269]
scenario4_losses = [576, 613, 270]

x = np.arange(len(crashes))
width = 0.2

bars1 = ax.bar(x - 1.5*width, scenario1_losses, width, label='Scenario 1 (20.66%)', color='#ff6b6b')
bars2 = ax.bar(x - 0.5*width, scenario2_losses, width, label='Scenario 2 (15%)', color='#ffd93d')
bars3 = ax.bar(x + 0.5*width, scenario3_losses, width, label='Scenario 3 (10%)', color='#4ecdc4')
bars4 = ax.bar(x + 1.5*width, scenario4_losses, width, label='Scenario 4 (50%)', color='#95e1d3')

ax.set_ylabel('Loss Amount (10,000 JPY)', fontsize=14, fontweight='bold')
ax.set_title('Historical Market Crash Simulation', fontsize=16, fontweight='bold')
ax.set_xticks(x)
ax.set_xticklabels(crashes, fontsize=12)
ax.legend(loc='upper left', fontsize=12)
ax.grid(axis='y', alpha=0.3)

# 値ラベル
for bars in [bars1, bars2, bars3, bars4]:
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 10,
                f'-{int(height)}', ha='center', va='bottom', fontsize=9, fontweight='bold')

plt.tight_layout()
plt.savefig(os.path.join(IMAGE_DIR, 'market_crash_simulation.png'), dpi=300, bbox_inches='tight')
print("Chart saved: market_crash_simulation.png")

print("\nAll charts generated successfully!")
