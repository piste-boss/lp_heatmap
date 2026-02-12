# クチコミGPT LP 再修正指示書

**作成日**: 2026年2月12日
**対象**: `/Users/ishikawasuguru/review-gpt-LP/index.html`, `styles.css`
**前提**: 抜本的改善レポート（20260212_review_gpt_lp_radical_improvement.md）に基づくLP刷新後のレビュー結果を反映

---

## 修正一覧

| # | 重要度 | 対象ファイル | 修正内容 |
|---|--------|-------------|----------|
| 1 | 高 | index.html | ヒーロー画像の追加 |
| 2 | 高 | index.html | セカンダリCTA（資料ダウンロード）の追加 |
| 3 | 中 | styles.css | Google Fonts 二重読み込みの解消 |
| 4 | 中 | styles.css | `.badge-label` / `.badge-value` の重複定義を削除 |
| 5 | 中 | index.html | 料金セクションとFAQの間に「安心ポイント」セクション追加 |
| 6 | 低 | styles.css | ヒーローセクションのPC時2カラム化 |

---

## 修正1: ヒーロー画像の追加【高】

### 背景
プランでは「広告のメインビジュアルと同じ画像をLPヒーローに使用」と明記。現状はテキスト+バッジのみで、広告→LPの視覚的連続性が欠けている。

### 対象
`index.html` — ヒーローセクション（L58-104付近）

### 修正内容
`.hero__content` 内に `.hero__text` と並列で `.hero__image` を追加する。

```html
<!-- hero__text の直後に追加 -->
<div class="hero__image">
  <picture>
    <source srcset="./assets/hero_main_v2.webp" type="image/webp">
    <img src="./assets/hero_main_v2.jpg" alt="Googleマップの高評価を確認する店舗オーナー" class="hero__image-img" loading="eager">
  </picture>
</div>
```

### CSS追加（styles.css）
```css
.hero__image {
  margin-top: 24px;
  text-align: center;
}

.hero__image-img {
  width: 100%;
  max-width: 480px;
  border-radius: 12px;
  box-shadow: var(--shadow-md);
}

/* PC: 2カラムレイアウト */
@media (min-width: 768px) {
  .hero__content {
    display: flex;
    align-items: center;
    gap: 40px;
  }
  .hero__text {
    flex: 1;
  }
  .hero__image {
    flex: 1;
    margin-top: 0;
  }
}
```

### 画像アセット
- `hero_main_v2.webp` / `hero_main_v2.jpg` — nanobanana pro で生成予定（20260212_review_prompt.md のプロンプト1-A参照）
- **画像が未完成の場合**: 現行の `hero_main.webp` をプレースホルダーとして使用可

---

## 修正2: セカンダリCTA（資料ダウンロード）の追加【高】

### 背景
プラン改善案C-2「コンバージョンポイントの多段階化」が未実施。LINE登録のみではハードルが高いユーザーを取りこぼしている。

### 対象
`index.html` — 料金セクションのCTA（L206-216付近）、最終CTAセクション（L268-278付近）

### 修正内容
既存のLINE CTAの下にセカンダリCTAを追加する。

#### 料金セクション（L216 `.cta-sub` の直後に追加）
```html
<a href="#contact" class="cta-secondary">
  まずは3分で読める資料を見る
</a>
```

#### 最終CTAセクション（L277 `.cta-sub` の直後に追加）
```html
<div class="cta-secondary-wrap">
  <span class="cta-or">または</span>
  <a href="mailto:info@piste-i.com?subject=クチコミGPT資料請求" class="cta-secondary">
    メールで資料を受け取る（無料）
  </a>
</div>
```

### CSS追加（styles.css）
```css
/* --- Secondary CTA --- */
.cta-secondary {
  display: inline-block;
  margin-top: 12px;
  color: var(--primary);
  font-size: 0.9rem;
  font-weight: 600;
  text-decoration: underline;
  text-underline-offset: 3px;
  transition: color 0.2s;
}

.cta-secondary:hover {
  color: var(--primary-light);
}

.cta-secondary-wrap {
  margin-top: 16px;
}

.cta-or {
  display: block;
  color: var(--muted);
  font-size: 0.8rem;
  margin-bottom: 4px;
}
```

### 備考
- 現段階では資料DL用のLP/フォームがないため、メール誘導またはページ内アンカーで代替
- 後日 Google フォーム or 専用資料DLページを用意した際にリンク先を差し替える

---

## 修正3: Google Fonts 二重読み込みの解消【中】

### 背景
`index.html` L17-20 の `<link>` タグと `styles.css` L5 の `@import` で同じフォントを二重読み込みしている。レンダリングブロックとなりパフォーマンスに影響。

### 対象
`styles.css` L5

### 修正内容
`styles.css` の `@import` 行を削除する。`<link>` タグの方が高速なため、HTML側のみで読み込む。

```css
/* 削除する行 */
@import url("https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;600;700&display=swap");
```

---

## 修正4: CSS 重複定義の削除【中】

### 背景
`.badge-label` と `.badge-value` が2回定義されており、2回目の定義（L351-364）が1回目（L330-349）の `text-shadow` と `z-index` を上書きして打ち消している。

### 対象
`styles.css` L351-364

### 修正内容
2回目の重複定義を削除する。

```css
/* 以下を削除（L351-364） */
.badge-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #ffffff;
  /* White Text */
  margin-bottom: 2px;
}

.badge-value {
  font-size: 1.1rem;
  font-weight: 800;
  color: #ffffff;
  /* White Text */
}
```

1回目の定義（L330-349）に `text-shadow` と `z-index: 1` が含まれており、光沢アニメーションの上にテキストを正しく表示するために必要。

---

## 修正5: 「安心ポイント」セクション追加【中】

### 背景
プラン改善案C-1では「FAQ（不安解消）」セクションに加え、Googleガイドライン準拠の安心訴求を重視。現FAQで触れてはいるが、スクロール途中の離脱防止として、料金の直後に簡潔な安心ポイントを入れるとCVR改善が見込める。

### 対象
`index.html` — 料金セクション（#pricing）とFAQセクション（#faq）の間

### 修正内容
```html
<!-- ===== 5.5 Trust Points ===== -->
<section class="section" id="trust">
  <div class="section__head">
    <h2>安心してご利用いただける理由</h2>
  </div>
  <div class="trust__grid">
    <div class="trust-card">
      <span class="trust-card__icon">&#x2705;</span>
      <h3>Googleガイドライン準拠</h3>
      <p>実際のお客様の感想をAIが言語化。投稿はお客様自身が行うため、規約に完全準拠しています。</p>
    </div>
    <div class="trust-card">
      <span class="trust-card__icon">&#x1F512;</span>
      <h3>長期縛りなし</h3>
      <p>効果が出なければ当月解約OK。導入リスクゼロでお試しいただけます。</p>
    </div>
    <div class="trust-card">
      <span class="trust-card__icon">&#x1F4AC;</span>
      <h3>専任チャットサポート</h3>
      <p>設定から運用まで、LINEチャットでいつでも相談可能。初期設定もお任せください。</p>
    </div>
  </div>
</section>
```

### CSS追加（styles.css）
```css
/* --- Trust Section --- */
.trust__grid {
  display: grid;
  gap: 16px;
}

.trust-card {
  background: var(--bg);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 24px;
  text-align: center;
  box-shadow: var(--shadow-sm);
}

.trust-card__icon {
  display: block;
  font-size: 2rem;
  margin-bottom: 12px;
}

.trust-card h3 {
  margin-bottom: 8px;
}

.trust-card p {
  color: var(--muted);
  font-size: 0.9rem;
  margin: 0;
}

@media (min-width: 768px) {
  .trust__grid {
    grid-template-columns: repeat(3, 1fr);
  }
}
```

---

## 修正6: バッジのデザイントーン調整【低】

### 背景
現在のバッジはゴールドグラデーション+光沢アニメーションで派手な印象。プランの「プロフェッショナルだが堅すぎない」「信頼感のあるネイビー」のトーンとやや乖離している。

### 対象
`styles.css` L281-328（`.hero__badge` 関連）

### 修正方針（2つの選択肢）

**A案: ネイビートーンに統一（推奨）**
```css
.hero__badge {
  /* ...既存のレイアウトプロパティは維持... */
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
  color: #ffffff;
  border: 3px solid var(--primary-subtle);
  box-shadow: 0 0 15px rgba(26, 54, 93, 0.3);
}
```
→ shineアニメーションは削除し、シンプルに。

**B案: 現行ゴールドを維持**
→ 「目を引く」効果はあるため、広告クリエイティブ側でも同じゴールドを使えば一貫性が保てる。

---

## 修正の優先順

```
1. [修正3] Google Fonts 二重読み込み解消  ← すぐ直せる、パフォーマンス改善
2. [修正4] CSS 重複定義の削除             ← すぐ直せる、バグ修正
3. [修正1] ヒーロー画像の追加             ← 画像生成後に実施
4. [修正2] セカンダリCTA追加              ← CV改善の核心
5. [修正5] 安心ポイントセクション          ← 離脱防止
6. [修正6] バッジトーン調整               ← デザイン統一（任意）
```

---

## 注意事項

- 修正1のヒーロー画像は `20260212_review_prompt.md` のプロンプトで nanobanana pro 生成後に差し込む
- 修正2のセカンダリCTAは、資料DLページが未作成のためメール誘導で暫定対応。後日差し替え前提
- 修正5の安心ポイントセクションは、セクション数が7→8に増えるが、各セクションが短いため全体の長さは許容範囲
- `src/main.js` や `netlify/functions/` 等のバックエンドは変更なし
