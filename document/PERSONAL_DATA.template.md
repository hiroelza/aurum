# 個人データ（PERSONAL_DATA.md）

**⚠️ このファイルはテンプレートです。記載されているデータはすべてサンプルデータです。**

**重要**: このファイルには個人識別情報が含まれています。外部共有厳禁。
**Git管理**: `.gitignore`で除外対象

**最終更新**: [UPDATE_DATE]

---

## 🚀 セットアップ手順

1. このファイルを `PERSONAL_DATA.md` にコピーしてください
   ```bash
   cp PERSONAL_DATA.template.md PERSONAL_DATA.md
   ```

2. 以下の `[...]` 部分を実際の値に置き換えてください

3. このファイル（PERSONAL_DATA.md）は `.gitignore` で除外されます

---

## 📋 基本情報

### 個人プロフィール
- **年齢**: [YOUR_AGE]歳（[CURRENT_YEAR]年[CURRENT_MONTH]月時点）
- **性別**: [YOUR_GENDER]
- **退職予定年齢**: [RETIREMENT_AGE]歳
- **退職予定年**: [RETIREMENT_YEAR]年

### 家族構成
- **配偶者**: [SPOUSE_STATUS]（[SPOUSE_AGE]歳、[SPOUSE_OCCUPATION]）
  - 就労予定: [SPOUSE_WORK_START_YEAR]年から（いない場合は削除）
  - 予定年収: 約[SPOUSE_ANNUAL_INCOME]万円
  - 配偶者のNISA口座: [SPOUSE_NISA_START_YEAR]年開設予定

- **子供1**: [CHILD1_NAME]（[CHILD1_AGE]歳、[CHILD1_HEALTH]）
  - 生年: [CHILD1_BIRTH_YEAR]年
  - 小学校入学予定: [CHILD1_ELEMENTARY_YEAR]年
  - 大学入学予定: [CHILD1_UNIVERSITY_YEAR]年（本人[YOUR_AGE_AT_CHILD1_UNI]歳時点）

- **子供2**: [CHILD2_NAME]（[CHILD2_AGE]歳、[CHILD2_HEALTH]）（いない場合は削除）
  - 生年: [CHILD2_BIRTH_YEAR]年
  - 小学校入学予定: [CHILD2_ELEMENTARY_YEAR]年
  - 大学入学予定: [CHILD2_UNIVERSITY_YEAR]年（本人[YOUR_AGE_AT_CHILD2_UNI]歳時点）

### 勤務先情報
- **職業**: [YOUR_OCCUPATION]
  - 例: 会社員、自営業、フリーランスなど
- **勤務先**: [YOUR_COMPANY]（[COMPANY_TYPE]）
  - 例: IT関連企業（東証プライム上場）、中小企業、ベンチャー企業など
- **居住地**: [YOUR_LOCATION]
  - 例: 東京都内、大阪府、神奈川県など
- **住居形態**: [HOUSING_TYPE]
  - 例: 賃貸、持ち家（ローンあり）、持ち家（ローンなし）
- **家賃**: 月[RENT_MONTHLY]万円（年間[RENT_ANNUAL]万円）
  - 持ち家の場合は「住宅ローン: 月[MORTGAGE_MONTHLY]万円」に変更

---

## 💰 収入情報

- **年収（税込）**: 約[ANNUAL_INCOME_GROSS]万円
- **年収（税引後）**: 約[ANNUAL_INCOME_NET]万円

---

## 💳 クレジットカード

- **メインカード**: [CARD_NAME]
  - 年会費: [CARD_ANNUAL_FEE]円（税込）
  - ポイント還元率: [CARD_POINT_RATE]
  - 継続特典: [CARD_BENEFITS]
  - 利用目的: [CARD_PURPOSE]
  - （不要な場合は削除してください）

---

## 📊 資産概要（サマリー）

**最終更新**: [ASSET_UPDATE_DATE]

### 総資産: [TOTAL_ASSETS]万円

| 資産区分 | 金額 | 構成比 |
|---------|------|--------|
| **NISA口座** | [NISA_ASSETS]万円 | [NISA_RATIO]% |
| **iDeCo** | [IDECO_ASSETS]万円 | [IDECO_RATIO]% |
| **投資資産計** | [INVESTMENT_TOTAL]万円 | [INVESTMENT_RATIO]% |
| **自社株** | [COMPANY_STOCK_ASSETS]万円 | [COMPANY_STOCK_RATIO]% |
| **現金** | [CASH_ASSETS]万円 | [CASH_RATIO]% |
| **総資産** | **[TOTAL_ASSETS]万円** | **100%** |

**📊 詳細データは以下を参照:**
- `INVESTMENT_PROFILE.md`: 投資方針、履歴、評価
- `sources/profile/asset_details.md`: 保有銘柄の詳細、取得単価、含み損益
- `sources/profile/investment_history.md`: 投資判断の履歴

---

## 💸 月次投資額

### 現在（[CURRENT_YEAR]年）
- **NISA**: 月[NISA_MONTHLY]万円
- **iDeCo**: 月[IDECO_MONTHLY]万円
- **合計**: 月[MONTHLY_INVESTMENT_TOTAL]万円（年間[ANNUAL_INVESTMENT_TOTAL]万円）

### 将来計画
- **[FUTURE_YEAR_1]年**: iDeCoを月[IDECO_INCREASED_MONTHLY]万円に増額（[IDECO_INCREASE_REASON]）
- **[FUTURE_YEAR_2]年**: 配偶者のNISAを月[SPOUSE_NISA_MONTHLY]万円開始（[SPOUSE_NISA_START_REASON]）
- （不要な場合は削除してください）

---

## 📌 重要な日付

- **退職予定**: [RETIREMENT_YEAR]年（[RETIREMENT_AGE]歳）
- **教育費必要時期**: [CHILD1_UNIVERSITY_YEAR]年（[CHILD1_NAME]大学入学）、[CHILD2_UNIVERSITY_YEAR]年（[CHILD2_NAME]大学入学）
- **配偶者の就労開始**: [SPOUSE_WORK_START_YEAR]年（該当する場合）
- **iDeCo増額**: [IDECO_INCREASE_YEAR]年（該当する場合）
- **配偶者のNISA開始**: [SPOUSE_NISA_START_YEAR]年（該当する場合）

---

## 💡 記入例

以下は架空のデータを使った記入例です:

```markdown
### 個人プロフィール
- **年齢**: 35歳（2025年11月時点）
- **性別**: 男性
- **退職予定年齢**: 65歳
- **退職予定年**: 2055年

### 収入情報
- **年収（税込）**: 約600万円
- **年収（税引後）**: 約450万円

### 資産概要
| 資産区分 | 金額 | 構成比 |
|---------|------|--------|
| **NISA口座** | 300万円 | 50.0% |
| **iDeCo** | 100万円 | 16.7% |
| **投資資産計** | 400万円 | 66.7% |
| **現金** | 200万円 | 33.3% |
| **総資産** | **600万円** | **100%** |
```

---

**参照元ファイル:**
- このファイルの情報は `INVESTMENT_PROFILE.md` および `.claude/01_project_overview.md` から抽出されています
- 投資判断時は、このファイルと `INVESTMENT_PROFILE.md` の両方を参照してください

---

**機密性:** 🔴 HIGH - 外部共有厳禁
