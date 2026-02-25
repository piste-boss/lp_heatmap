# Gemini ヒートマップデータ採取指示書 — review_gpt

**日付:** 2026-02-25
**対象LP:** review_gpt (https://review-gpt-lp.netlify.app/)

---

## タスク概要

Microsoft Clarityから review_gpt のヒートマップデータを採取し、以下のディレクトリに保存してください。

**保存先:** `/Users/ishikawasuguru/lp_heatmap/review_gpt/`

---

## 収集手順

### 1. Clarityダッシュボードへアクセス

1. Microsoft Clarityにログイン
2. review_gpt プロジェクトを選択
3. 分析期間を **2026-02-18 〜 2026-02-24（7日間）** に設定

### 2. データ収集

#### 2.1 スクロールヒートマップ
- 各地点での離脱率を記録
- **スクリーンショット**: `/Users/ishikawasuguru/lp_heatmap/review_gpt/20260225_scroll.png`

#### 2.2 アテンションヒートマップ
- 各エリアの滞在時間を記録
- **スクリーンショット**: `/Users/ishikawasuguru/lp_heatmap/review_gpt/20260225_attention.png`

#### 2.3 クリックヒートマップ
- デッドクリックを特定
- **モバイル**: `/Users/ishikawasuguru/lp_heatmap/review_gpt/20260225_click_mobile.png`
- **デスクトップ**: `/Users/ishikawasuguru/lp_heatmap/review_gpt/20260225_click_desktop.png`

#### 2.4 セッション録画
- 2-3件確認、離脱ポイント・混乱の兆候を記録

### 3. データファイルの作成

**ファイル:** `/Users/ishikawasuguru/lp_heatmap/review_gpt/20260225_clarity_data.md`

```markdown
# review_gpt Clarityデータ — 2026-02-25

## 分析期間
2026-02-18 〜 2026-02-24

## 基本指標
- セッション数:
- ページビュー数:
- 平均滞在時間:
- 直帰率:
- デバイス比率（モバイル/デスクトップ）:

## スクロールヒートマップ
- 25%到達率:
- 50%到達率:
- 75%到達率:
- 100%到達率:
- 主要離脱ポイント:
- スクリーンショット: ![scroll](20260225_scroll.png)

## アテンションヒートマップ
- 最も注目されているセクション:
- 注目度が低いセクション:
- スクリーンショット: ![attention](20260225_attention.png)

## クリックヒートマップ
### モバイル
- 最もクリックされている要素:
- デッドクリック:
- スクリーンショット: ![click_mobile](20260225_click_mobile.png)

### デスクトップ
- 最もクリックされている要素:
- デッドクリック:
- スクリーンショット: ![click_desktop](20260225_click_desktop.png)

## セッション録画の知見
### セッション1
- デバイス:
- 滞在時間:
- 行動パターン:
- 離脱ポイント:

### セッション2
- デバイス:
- 滞在時間:
- 行動パターン:
- 離脱ポイント:
```

---

## 関連データ

Google Ads週次レポートが `/Users/ishikawasuguru/ai_google_ads/ads_repo/20260225.md` に保存済みです。
LP解析時にこのデータも活用します。

## 完了後

「review_gpt のClarityデータ採取完了」と Claude Code に伝えてください。
