---
name: LP解析とレポート作成
description: Clarity Export APIまたはClarityダッシュボードからデータを取得してコンバージョン改善レポートを作成し、指定ディレクトリに保存するスキル。Piste系LPではInstagram広告データ、review_gptではGoogle Ads広告データも統合分析する。
---

# LP解析とレポート作成スキル

このスキルは、Microsoft Clarityのデータを活用してランディングページ（LP）を解析し、コンバージョン改善のための詳細レポートを作成します。

**広告データ統合:**
- **Piste_lp / piste_over40**: Instagram広告データ（`/Users/ishikawasuguru/insta_piste/add_repo`）と統合分析
- **review_gpt**: Google Ads広告データ（`/Users/ishikawasuguru/ai_google_ads/ads_repo`）と統合分析

## 対象プロジェクト一覧

| LP名 | URL | Clarity プロジェクトID | 広告種別 |
|------|-----|----------------------|---------|
| piste_lp | https://piste-lp.netlify.app/ | 3150700034083084 | Instagram |
| piste_over40 | https://piste-lp-40.netlify.app/ | 3177852411005894 | Instagram |
| review_gpt | https://review-gpt-lp.netlify.app/ | 3175348461854130 | Google Ads |

## 前提条件

- Clarity Data Export APIのJWTトークン（各プロジェクトごとに必要）
- **【Piste系LP】** `/Users/ishikawasuguru/insta_piste/add_repo` にInstagram広告レポートが保存済み
- **【review_gpt】** `/Users/ishikawasuguru/ai_google_ads/ads_repo` にGoogle Ads週次レポートが保存済み

## スキルの流れ

### ステップ1: Clarity Export APIでデータ取得（推奨）

Clarity Data Export APIを使って定量データを取得する。APIが利用可能な場合はこちらを優先する。

#### 1.1 APIエンドポイント

```
GET https://www.clarity.ms/export-data/api/v1/project-live-insights
```

#### 1.2 認証

```
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
```

JWTトークンはClarityプロジェクトの Settings → Data Export → Generate new API token で発行する。各プロジェクトごとに個別のトークンが必要。

#### 1.3 必須クエリ（3回のAPIコール）

各プロジェクトに対して以下の3つのリクエストを実行する:

1. **URL別分析**: `?numOfDays=3&dimension1=URL`
   - 取得: ページ別トラフィック、スクロール深度、エンゲージメント、UXエラー
2. **デバイス別分析**: `?numOfDays=3&dimension1=Device`
   - 取得: Mobile/PC/Tablet別のトラフィック、スクロール深度、エンゲージメント
3. **チャネル別分析**: `?numOfDays=3&dimension1=Channel`
   - 取得: PaidSearch/Social/Direct等のチャネル別パフォーマンス

#### 1.4 curlコマンド例

```bash
curl -s "https://www.clarity.ms/export-data/api/v1/project-live-insights?numOfDays=3&dimension1=URL" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" | python3 -m json.tool
```

#### 1.5 レスポンスから抽出する指標

| メトリクス名 | 抽出する値 |
|------------|----------|
| Traffic | totalSessionCount, totalBotSessionCount, distinctUserCount, pagesPerSessionPercentage |
| ScrollDepth | averageScrollDepth |
| EngagementTime | totalTime, activeTime |
| DeadClickCount | sessionsWithMetricPercentage |
| RageClickCount | sessionsWithMetricPercentage |
| QuickbackClick | sessionsWithMetricPercentage |
| ExcessiveScroll | sessionsWithMetricPercentage |
| ScriptErrorCount | sessionsWithMetricPercentage |
| ErrorClickCount | sessionsWithMetricPercentage |

#### 1.6 API制限事項

- `numOfDays` は **1, 2, 3** のみ（直近1〜3日間のデータ）
- 1プロジェクトあたり **1日10リクエストまで**
- 最大 **3つのdimension** を同時指定可能
- レスポンスは最大1,000行
- **ヒートマップ画像・セッション録画はAPIでは取得不可**

### ステップ1（代替）: Clarityダッシュボードでデータ収集

APIが利用できない場合、またはヒートマップ画像・セッション録画が必要な場合は、Gemini用指示書を作成してClarityダッシュボードからデータを収集する。

指示書の保存先: `/Users/ishikawasuguru/lp_heatmap/gemini_instructions_YYYYMMDD_[lp_name].md`

#### 収集項目

- **スクロールヒートマップ**: 各地点での離脱率、スクリーンショット
- **アテンションヒートマップ**: 各エリアの滞在時間、スクリーンショット
- **クリックヒートマップ**: クリック要素、デッドクリック、デバイス別分析
- **セッション録画**: ユーザー行動パターン2-3件、離脱ポイント特定

### ステップ2: 広告データの読み取り

#### 2.1 Piste系LP（piste_lp / piste_over40）→ Instagram広告

1. `/Users/ishikawasuguru/insta_piste/add_repo` 内のレポートを確認
2. Clarity分析期間と同一期間（または最も近い期間）の広告レポートを特定
   - ファイル命名規則: `YYYYMMDD_YYYYMMDD_weekly_ads_analysis.md` または `YYYYMMDD_piste_ads_analysis.md`
3. 抽出データ:
   - 全体サマリー: 消化金額、Imp、クリック数、CPC、CTR
   - セグメント別比較: U40 vs Over40
   - クリエイティブ別詳細: CTR、CPC、予算シェア、信頼度
   - アクション提案

#### 2.2 review_gpt → Google Ads

1. `/Users/ishikawasuguru/ai_google_ads/ads_repo` 内のレポートを確認
2. Clarity分析期間と同一期間（または最も近い期間）の週次レポートを特定
   - ファイル命名規則: `YYYYMMDD.md`
3. 抽出データ:
   - エグゼクティブサマリー: 費用、クリック数、表示回数、CTR、CPC、CV
   - 前週比: 各指標の変化率
   - 日別パフォーマンス推移
   - キャンペーン別パフォーマンス
   - 課題分析・改善提案

#### 期間の照合方法
- 広告レポートの期間とClarity分析期間を照合
- 完全一致しない場合は最も近い期間のレポートを使用し、ずれをレポートに明記

### ステップ3: データ分析と問題点の特定

#### 3.1 クリティカルな問題（優先度：最高）
- 広告クリック数 vs Clarityセッション数の乖離（Clarityタグ不備の可能性）
- 初動離脱率が30%以上（スクロール深度10%未満）
- コンバージョン阻害要因

#### 3.2 重要な問題（優先度：高）
- チャネル別エンゲージメント差（PaidSearch vs Social等）
- 広告メッセージとLPファーストビューの不整合
- ユーザーの迷いや混乱

#### 3.3 改善推奨（優先度：中）
- UX最適化の余地
- デザイン改善点
- UTMパラメータの整理

#### 3.4 広告×LP統合分析
- **広告→LP遷移の一貫性**: 広告クリエイティブとLPファーストビューのメッセージ整合性
- **チャネル別LP行動**: 広告経由 vs オーガニック経由のスクロール・エンゲージメント差
- **費用対効果**: 広告費用あたりのLP到達率・コンバージョン効率
- **【Piste系LP】セグメント別**: Over40 vs U40 の広告CTRとLP行動の相関
- **【review_gpt】チャネル別**: PaidSearch vs Social のエンゲージメント差異分析

### ステップ4: 修正案の立案

#### 4.1 Quick Wins（1週間以内）
- インパクト高・実装難易度低の施策

#### 4.2 中期的改善（2-4週間）
- 構造的な改善施策

#### 4.3 継続的改善
- A/Bテストや長期最適化

### ステップ5: レポートの作成

以下の構成でマークダウンレポートを作成：

```markdown
# [LP名] 解析レポートと修正案

## サマリー
- ターゲット
- コンバージョン定義
- 現状パフォーマンス

## Clarityデータ分析結果
- トラフィック概要（セッション数、ユニークユーザー、PV/セッション）
- デバイス別分析
- チャネル別パフォーマンス（スクロール深度、滞在時間、アクティブ時間の比較）
- スクロールデータ
- エンゲージメント
- UXエラー指標
- ※APIデータの場合はヒートマップ画像なし。ダッシュボードデータの場合は画像付き

## 広告データ分析結果
### Piste系LP → Instagram広告
- 全体パフォーマンス: 消化金額、CPC、CTR
- セグメント別比較（U40 vs Over40）
- クリエイティブ別パフォーマンス

### review_gpt → Google Ads
- 全体パフォーマンス: 費用、クリック数、表示回数、CTR、CPC、CV
- 前週比
- 日別推移

## 広告×LP統合分析
- 広告クリック vs Clarityセッションの整合性
- チャネル別エンゲージメント差
- 広告費用対効果の評価

## 問題点の特定
- クリティカル、重要、改善推奨に分類

## 修正案（優先度順）
- Quick Wins / 中期的改善 / 継続的改善

## 優先度マトリクス
- 表形式（インパクト × 実装難易度）

## 実装ロードマップ
- フェーズ1-3に分けた計画

## 次のステップ
```

### ステップ6: ファイル保存

レポートを保存：

**プロジェクトディレクトリ**:
```
/Users/ishikawasuguru/lp_heatmap/[YYYYMMDD][lp_name].md
```

## 出力ファイル命名規則

- フォーマット: `YYYYMMDD` + `lp_name` + `.md`
- 例: `20260304piste_lp.md`, `20260304review_gpt.md`

## 重要なポイント

### データ収集の優先順位
1. **Clarity Export API**（推奨）: 定量データの自動取得。高速だが直近1-3日間・ヒートマップ画像なし
2. **Clarityダッシュボード**（補完）: ヒートマップ画像・セッション録画が必要な場合。Gemini指示書を作成

### データ収集時の注意点
- **デバイス別分析**: モバイルとデスクトップで行動が異なる場合がある
- **チャネル別分析**: PaidSearch vs Social vs Direct で大きな差が出ることが多い（review_gptで顕著）
- **広告クリック vs Clarityセッションの乖離**: Clarityタグの設置不備を示す重要なシグナル
- **広告データとの期間一致**: Clarity分析期間と広告レポートの期間を一致させる。ずれがある場合はレポートに明記

### レポート作成時の注意点
- **データに基づく**: 推測ではなく実際のデータを根拠にする
- **具体的な提案**: 「改善すべき」ではなく「こう変更する」と明記
- **優先順位付け**: インパクトと実装難易度でマトリクス化
- **3プロジェクト横断比較**: 可能な場合、piste_lp / piste_over40 / review_gptの横断比較テーブルを含める

## 広告データ参照先

### Piste系LP
- **ディレクトリ**: `/Users/ishikawasuguru/insta_piste/add_repo`
- **ファイル命名規則**: `YYYYMMDD_YYYYMMDD_weekly_ads_analysis.md` または `YYYYMMDD_piste_ads_analysis.md`
- **データ内容**: Instagram/Meta広告データ（CPC、CTR、消化金額、セグメント別比較、クリエイティブ別詳細）

### review_gpt
- **ディレクトリ**: `/Users/ishikawasuguru/ai_google_ads/ads_repo`
- **ファイル命名規則**: `YYYYMMDD.md`
- **データ内容**: Google Ads週次レポート（費用、クリック数、表示回数、CTR、CPC、CV、前週比、日別推移）

## トラブルシューティング

### Export APIがエラーを返す
- JWTトークンの有効期限を確認（`exp`フィールド）
- `numOfDays`が1, 2, 3のいずれかであることを確認
- `Content-Type: application/json`ヘッダーが含まれているか確認
- 1日のリクエスト上限（10回/プロジェクト）に達していないか確認

### 広告クリック数とClarityセッション数が大きく乖離する
- ClarityタグがLPに正しく設置されているか確認
- ページ読み込み速度を確認（遅いとClarityタグ発火前に離脱）
- IG広告のClick指標にはプロフィールクリック等の非LP遷移も含まれる場合がある

### Clarityでデータが表示されない
- プロジェクトが作成されているか確認
- トラッキングコードが正しく設置されているか確認
- データ収集に最低24-48時間必要

## 関連スキル

- なし（このスキルは独立して使用可能）

## 更新履歴

- 2026-03-04: Clarity Export API対応を追加。review_gptのGoogle Ads統合分析を追加。プロジェクト一覧テーブルを追加
- 2026-02-22: Piste系LP（piste_lp, piste_over40）でInstagram広告データの統合分析機能を追加
- 2026-02-10: 初版作成
