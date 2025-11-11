# エージェント作成ガイドライン

<!-- 動作確認: Windows Defender除外設定後、Editツール正常動作 ✅✅✅ (3回連続成功) -->

このディレクトリには、aurumプロジェクト専用の投資関連エージェントが配置されています。

## 現在のエージェント

### 投資評価エージェント（3エージェント評価システム）

1. **investment-advisor-hayato.md** - 伊藤ハヤト投資哲学評価者
   - 役割: 投資判断が7つの原則に合致しているか評価
   - スコアリング: 0-100点、支持度0-100%

2. **investment-researcher.md** - 統計データ分析者
   - 役割: 市場データ、統計分析、モンテカルロシミュレーション
   - スコアリング: 0-100点、支持度0-100%

3. **investment-advisor-japanese.md** - 日本税制・ライフプラン専門家
   - 役割: 日本の税制、NISA/iDeCo、ライフプラン適合性評価
   - スコアリング: 0-100点、支持度0-100%

### 市場分析エージェント

4. **us-market-analyst.md** - 米国市場分析専門家
   - 役割: 米国株式市場の分析、調査、トレンド評価

### 成長支援エージェント

5. **growth-advisor.md** - 率直な助言者（投資判断・人生設計専用）
   - 役割: 前提を問い直し、盲点を指摘し、機会費用を定量化する
   - 特徴: 過度な肯定を避け、客観的真実を優先
   - 適用範囲: 投資判断、人生設計、リスク評価（技術タスクには不使用）
   - 使用例:
     ```bash
     # 投資判断の検証
     "NVIDIA株を買い増ししたいが、Growth Advisorで評価してください"

     # 人生設計の妥当性確認
     "老後資金計画をGrowth Advisorでレビューしてください"
     ```
   - 呼び出しタイミング:
     - **明示的な呼び出し**: ユーザーが「Growth Advisorで」と指定した場合
     - **状況判断による呼び出し**: 感情的判断が疑われる場合、重要な投資判断で客観的評価が必要と判断される場合
     - **重要**: 率直な批判を行うため、技術的なタスクや単純な情報取得には使用しない

---

## 新規エージェント作成手順

### 1. ファイル名の決定

**命名規則**: `{category}-{specific-role}.md`

**例**:
- `investment-advisor-hayato.md` (投資アドバイザー - ハヤト)
- `us-market-analyst.md` (米国市場 - アナリスト)

### 2. フロントマター（YAML）の作成

すべてのエージェントファイルは、以下のYAMLフロントマターで始める必要があります：

```yaml
---
name: {agent-name}
description: Use this agent when {usage description}. Examples:

<example>
Context: {context description}
user: "{user query example in Japanese}"
assistant: "{assistant response showing agent invocation}"
<commentary>
{explanation of why this agent is appropriate}
</commentary>
</example>

{2-3 more examples}

model: sonnet
---
```

**必須フィールド**:
- `name`: エージェント名（ファイル名の拡張子なし部分と一致）
- `description`: エージェントの使用目的と例
- `model`: 使用するモデル（`sonnet`、`opus`、`haiku`）

### 3. エージェント本体の構成

#### 最小構成

```markdown
You are {role description}.

**Knowledge Base (用語集):**
評価時に必要な専門用語の定義については、以下の用語集を参照してください:
- **コア金融用語**: `.claude/glossaries/core-financial-terms.md`
  {description}
- **{specific glossary}**: `.claude/glossaries/{filename}.md`
  {description}

{Core competencies section}

{Analysis framework section}

{Communication style section}

{Critical guidelines section}
```

#### 推奨セクション

1. **プロジェクトコンテキスト** (投資エージェントの場合)
   - 役割と目的
   - INVESTMENT_PROFILE.mdの参照タイミング
   - 3エージェント評価システムにおける位置づけ

2. **Knowledge Base (用語集)** - 必須
   - 参照する用語集を明記
   - 各用語集の対象範囲を説明

3. **Core Competencies**
   - エージェントの専門分野
   - 得意な分析手法

4. **Analysis Framework**
   - 分析の手順
   - 評価基準

5. **Communication Style**
   - 応答スタイル
   - 言語（日本語 or 英語）

6. **Critical Guidelines**
   - 重要な注意事項
   - やってはいけないこと

7. **ツール使用ガイドライン** (オプション)
   - WebSearch、WebFetch、Read、Bashの使い分け

### 4. 用語集参照の追加

**投資関連エージェントの場合**、必ず以下を含める：

```markdown
**Knowledge Base (用語集):**
評価時に必要な専門用語の定義については、以下の用語集を参照してください:
- **コア金融用語**: `.claude/glossaries/core-financial-terms.md`
  投資商品、リスク指標、リターン指標、ファンダメンタル分析指標など
- **投資哲学用語**: `.claude/glossaries/investment-philosophy-terms.md`
  伊藤ハヤト氏の投資哲学、投資原則、リスク管理概念など
```

米国市場分析の場合は追加で：
```markdown
- **米国市場用語**: `.claude/glossaries/us-market-terms.md`
  米国株式市場特有の指数、制度、市場セグメント、規制機関など
```

---

## テンプレート

以下のテンプレートをコピーして使用してください：

```markdown
---
name: {agent-name}
description: Use this agent when {description}. Examples:

<example>
Context: {context}
user: "{user query}"
assistant: "{response}"
<commentary>{explanation}</commentary>
</example>

model: sonnet
---

You are {role description}.

**Knowledge Base (用語集):**
評価時に必要な専門用語の定義については、以下の用語集を参照してください:
- **コア金融用語**: `.claude/glossaries/core-financial-terms.md`
  投資商品、リスク指標、リターン指標など

**Core Competencies:**
- {competency 1}
- {competency 2}

**Analysis Framework:**
1. {step 1}
2. {step 2}

**Communication Style:**
- {style 1}
- {style 2}

**Critical Guidelines:**
- {guideline 1}
- {guideline 2}

**最終更新**: {date}
```

---

## チェックリスト

新規エージェント作成時、以下を確認してください：

- [ ] ファイル名が命名規則に従っている
- [ ] YAMLフロントマターが正しい
- [ ] `name`フィールドがファイル名と一致
- [ ] `description`に2-3個の例が含まれている
- [ ] **Knowledge Base (用語集)** セクションがある
- [ ] 用語集の参照パスが正しい（`.claude/glossaries/{filename}.md`）
- [ ] モデル指定が適切（`sonnet`、`opus`、`haiku`）
- [ ] 日本語/英語の使い分けが適切
- [ ] 最終更新日が記載されている

---

## 参考資料

### 既存エージェントの参照

- **investment-advisor-hayato.md** - 投資哲学評価の模範
- **us-market-analyst.md** - 市場分析エージェントの模範（最も詳細）
- **investment-researcher.md** - 統計分析エージェントの模範

### ドキュメント

- `.claude/glossaries/` - 用語集ファイル
- `.claude/01_project_overview.md` - プロジェクト概要、投資哲学
- `.claude/03_work_process.md` - サブエージェント議論フレームワーク

---

**最終更新**: 2025年11月5日（growth-advisor呼び出しルール更新、Defender除外設定後の動作確認）
