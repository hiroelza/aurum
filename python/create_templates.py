#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
テンプレートファイル作成スクリプト

INVESTMENT_PROFILE.md、asset_details.md、investment_history.mdから
テンプレートファイルを作成します。
"""

import re
from pathlib import Path

def create_investment_profile_template():
    """INVESTMENT_PROFILE.template.mdを作成"""

    # 元ファイルを読み込み
    with open('INVESTMENT_PROFILE.md', 'r', encoding='utf-8') as f:
        content = f.read()

    # 個人情報をプレースホルダーに置換
    # 注意: 以下の例はdocument/examples.md Case 1（独身35歳）を参考にしています
    replacements = {
        # 年齢・年
        r'35歳': '[YOUR_AGE]歳',
        r'65歳': '[RETIREMENT_AGE]歳',
        r'2055年': '[RETIREMENT_YEAR]年',
        r'2025年11月時点': '[CURRENT_YEAR]年[CURRENT_MONTH]月時点',
        r'2048年': '[CHILD1_UNIVERSITY_YEAR]年',
        r'2050年': '[CHILD2_UNIVERSITY_YEAR]年',

        # 家族構成（独身の例を基本とする）
        r'配偶者（なし）': '配偶者（[SPOUSE_AGE]歳、いない場合は None）',
        r'子供（なし）': '子供1（[CHILD1_AGE]歳、いない場合は None）',
        r'2015年': '[CHILD1_BIRTH_YEAR]年',
        r'2017年': '[CHILD2_BIRTH_YEAR]年',

        # 収入・資産（examples.md Case 1の値を使用）
        r'約600万円（税込）': '約[ANNUAL_INCOME_GROSS]万円（税込）',
        r'約450万円': '約[ANNUAL_INCOME_NET]万円',
        r'800万円': '[TOTAL_ASSETS]万円',
        r'500万円': '[NISA_ASSETS]万円',
        r'100万円': '[IDECO_ASSETS]万円',
        r'600万円': '[INVESTMENT_TOTAL]万円',
        r'0万円': '[COMPANY_STOCK_ASSETS]万円',
        r'200万円': '[CASH_ASSETS]万円',

        # 勤務先・居住地（架空のデータ）
        r'株式会社サンプル': '[YOUR_COMPANY]',
        r'東京都': '[YOUR_LOCATION]',
        r'月10万円': '月[RENT_MONTHLY]万円',

        # その他具体的な数値（examples.md Case 1に統一）
        r'月5万円': '月[NISA_MONTHLY]万円',
        r'月2\.0万円': '月[IDECO_MONTHLY]万円',
        r'月2\.5万円': '月[IDECO_INCREASED_MONTHLY]万円',
        r'2027年': '[IDECO_INCREASE_YEAR]年',
        r'2028年': '[SPOUSE_WORK_START_YEAR]年',
        r'月0万円': '月[SPOUSE_NISA_MONTHLY]万円',
    }

    # 置換実行
    for pattern, replacement in replacements.items():
        content = re.sub(pattern, replacement, content)

    # ヘッダーにセットアップ手順を追加
    header = """# 投資プロフィール・マスターファイル（テンプレート）

**このファイルはテンプレートです。**

## 🚀 セットアップ手順

1. このファイルを `INVESTMENT_PROFILE.md` にコピーしてください
   ```bash
   cp INVESTMENT_PROFILE.template.md INVESTMENT_PROFILE.md
   ```

2. 以下の `[...]` 部分を実際の値に置き換えてください

3. このファイル（INVESTMENT_PROFILE.md）は `.gitignore` で除外されます

4. 詳細データは以下も設定してください:
   - `sources/profile/asset_details.md` - 保有銘柄の詳細
   - `sources/profile/investment_history.md` - 投資判断の履歴

---

"""

    # ヘッダーを追加（元の「最終更新日」行の後に挿入）
    content = re.sub(
        r'(\*\*最終更新日:\*\* .*?\n)',
        r'\1\n' + header,
        content,
        count=1
    )

    # ファイルに書き込み
    with open('INVESTMENT_PROFILE.template.md', 'w', encoding='utf-8') as f:
        f.write(content)

    print('✅ INVESTMENT_PROFILE.template.md created')


def create_asset_details_template():
    """asset_details.template.mdを作成（簡易版）"""

    template_content = """# 資産詳細データ（テンプレート）

**このファイルはテンプレートです。**

## 🚀 セットアップ手順

1. このファイルを `asset_details.md` にコピーしてください
   ```bash
   cp asset_details.template.md asset_details.md
   ```

2. 以下のサンプルデータを参考に、あなたの保有資産を記入してください

3. このファイル（asset_details.md）は `.gitignore` で除外されます

---

## 📊 NISA口座（サンプル）

### 保有銘柄一覧

| 銘柄名 | ファンドコード | 取得口数 | 取得単価 | 取得総額 | 評価単価 | 評価額 | 含み損益 | リターン率 |
|--------|--------------|---------|---------|---------|---------|--------|---------|----------|
| eMAXIS Slim 全世界株式 | 03311187 | 1,000,000 | 15,000 | 150万円 | 18,000 | 180万円 | +30万円 | +20.0% |
| eMAXIS Slim 米国株式（S&P500） | 03312127 | 500,000 | 20,000 | 100万円 | 24,000 | 120万円 | +20万円 | +20.0% |

**合計:**
- 取得総額: 250万円
- 評価額: 300万円
- 含み損益: +50万円
- リターン率: +20.0%

---

## 💼 iDeCo（サンプル）

### 保有銘柄一覧

| 銘柄名 | ファンドコード | 取得口数 | 取得単価 | 取得総額 | 評価単価 | 評価額 | 含み損益 | リターン率 |
|--------|--------------|---------|---------|---------|---------|--------|---------|----------|
| 楽天・全世界株式インデックス・ファンド | - | 300,000 | 15,000 | 45万円 | 18,000 | 54万円 | +9万円 | +20.0% |

**合計:**
- 取得総額: 45万円
- 評価額: 54万円
- 含み損益: +9万円
- リターン率: +20.0%

---

## 🏢 自社株（サンプル）

- **銘柄名**: [YOUR_COMPANY]
- **証券コード**: [COMPANY_CODE]
- **保有株数**: [SHARES]株
- **簿価単価**: [BOOK_VALUE]円
- **取得総額**: [TOTAL_BOOK_VALUE]万円
- **現在株価**: [CURRENT_PRICE]円
- **評価額**: [MARKET_VALUE]万円
- **含み損益**: [UNREALIZED_GAIN]万円
- **リターン率**: [RETURN_RATE]%

---

## 記入例

以下は架空のデータを使った記入例です:

```markdown
### 保有銘柄一覧

| 銘柄名 | ファンドコード | 取得口数 | 取得単価 | 取得総額 | 評価単価 | 評価額 | 含み損益 | リターン率 |
|--------|--------------|---------|---------|---------|---------|--------|---------|----------|
| eMAXIS Slim 全世界株式 | 03311187 | 2,500,000 | 14,500 | 362.5万円 | 17,800 | 445万円 | +82.5万円 | +22.8% |
```

---

**最終更新**: [UPDATE_DATE]
"""

    with open('sources/profile/templates/asset_details.template.md', 'w', encoding='utf-8') as f:
        f.write(template_content)

    print('✅ sources/profile/templates/asset_details.template.md created')


def create_investment_history_template():
    """investment_history.template.mdを作成（簡易版）"""

    template_content = """# 投資判断履歴（テンプレート）

**このファイルはテンプレートです。**

## 🚀 セットアップ手順

1. このファイルを `investment_history.md` にコピーしてください
   ```bash
   cp investment_history.template.md investment_history.md
   ```

2. 以下のサンプルを参考に、あなたの投資判断履歴を記入してください

3. このファイル（investment_history.md）は `.gitignore` で除外されます

---

## 📝 投資判断履歴

### [YYYY年MM月DD日]: [投資商品名]の購入判断

**判断内容**: [具体的な投資判断内容]

**3エージェント評価**:

| エージェント | スコア | 支持度 | 主な理由 |
|-------------|--------|--------|---------|
| hayato      | XX/100 | XX%    | [伊藤ハヤト氏の投資哲学との整合性] |
| researcher  | XX/100 | XX%    | [統計データ・過去実績に基づく分析] |
| japanese    | XX/100 | XX%    | [日本の税制・ライフプラン適合性] |

**総合評価**: XX/100点（平均）

**最終判断**: [実施 / 見送り / 条件付き実施]

**実施理由**: [判断の根拠を記載]

**結果**: [実施後の結果を記載（後日更新）]

---

## 記入例

以下は架空のデータを使った記入例です:

### 2024年11月15日: eMAXIS Slim 全世界株式の積立開始

**判断内容**: NISA成長投資枠で月10万円の積立を開始

**3エージェント評価**:

| エージェント | スコア | 支持度 | 主な理由 |
|-------------|--------|--------|---------|
| hayato      | 95/100 | 100%   | 低コスト・全世界分散・パッシブ運用で完全に一致 |
| researcher  | 90/100 | 95%    | 過去20年のデータで年率7%のリターン実績 |
| japanese    | 92/100 | 98%    | NISA枠を最大活用、税制優遇を受けられる |

**総合評価**: 92/100点（平均）

**最終判断**: 実施

**実施理由**:
- 3エージェントすべてが高評価
- 投資哲学に完全に合致
- NISA枠の有効活用

**結果**:
- 積立開始から6ヶ月経過
- リターン率: +12.5%（想定を上回る）
- 継続中

---

## 📊 投資判断の統計

### 総括（サンプル）

- **総判断数**: [TOTAL_DECISIONS]件
- **実施**: [IMPLEMENTED]件
- **見送り**: [PASSED]件
- **条件付き実施**: [CONDITIONAL]件

### 平均スコア

- **hayato**: [HAYATO_AVG]/100点
- **researcher**: [RESEARCHER_AVG]/100点
- **japanese**: [JAPANESE_AVG]/100点
- **総合**: [OVERALL_AVG]/100点

---

**最終更新**: [UPDATE_DATE]
"""

    with open('sources/profile/templates/investment_history.template.md', 'w', encoding='utf-8') as f:
        f.write(template_content)

    print('✅ sources/profile/templates/investment_history.template.md created')


if __name__ == '__main__':
    print('Creating template files...\n')

    create_investment_profile_template()
    create_asset_details_template()
    create_investment_history_template()

    print('\n✅ All template files created successfully!')
    print('\nCreated files:')
    print('  - INVESTMENT_PROFILE.template.md')
    print('  - sources/profile/templates/asset_details.template.md')
    print('  - sources/profile/templates/investment_history.template.md')
