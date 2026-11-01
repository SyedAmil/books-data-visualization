"""
Task 3: Data Visualization on books data
Run in the same folder as the CSV:  python visualize_books.py
Outputs: 4 charts, dashboard.png and data_story.md
"""
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid", palette="viridis")
df = pd.read_csv("books_viz_data.csv")
df["price_band"] = pd.cut(df["price_gbp"], bins=[0, 20, 30, 40, 50, 100],
                          labels=["<20", "20-30", "30-40", "40-50", "50+"])

# Chart 1: how are ratings spread?
def chart_ratings(ax):
    sns.countplot(data=df, x="rating", ax=ax)
    ax.set_title("Number of books per rating")
    ax.set_xlabel("Rating (stars)"); ax.set_ylabel("Books")
    for c in ax.containers:
        ax.bar_label(c)

# Chart 2: how are prices spread?
def chart_prices(ax):
    sns.histplot(df["price_gbp"], bins=30, kde=True, ax=ax)
    ax.axvline(df["price_gbp"].mean(), color="red", ls="--", label="Average")
    ax.set_title("Price distribution"); ax.set_xlabel("Price (GBP)")
    ax.legend()

# Chart 3: does price change with rating?
def chart_box(ax):
    sns.boxplot(data=df, x="rating", y="price_gbp", ax=ax)
    ax.set_title("Price by rating"); ax.set_xlabel("Rating (stars)")
    ax.set_ylabel("Price (GBP)")

# Chart 4: rating mix inside each price band
def chart_heat(ax):
    table = pd.crosstab(df["price_band"], df["rating"])
    sns.heatmap(table, annot=True, fmt="d", cmap="YlGnBu", ax=ax)
    ax.set_title("Books by price band and rating")
    ax.set_xlabel("Rating (stars)"); ax.set_ylabel("Price band (GBP)")

charts = [("chart_ratings.png", chart_ratings), ("chart_prices.png", chart_prices),
          ("chart_price_by_rating.png", chart_box), ("chart_heatmap.png", chart_heat)]

for name, fn in charts:
    fig, ax = plt.subplots(figsize=(7, 4.5))
    fn(ax)
    fig.savefig(name, dpi=130, bbox_inches="tight")
    plt.close(fig)

# Dashboard: all four charts on one page
fig, axes = plt.subplots(2, 2, figsize=(14, 9))
for ax, (_, fn) in zip(axes.flat, charts):
    fn(ax)
fig.suptitle("Books Dashboard: 1,000 books from books.toscrape.com", fontsize=16)
fig.tight_layout()
fig.savefig("dashboard.png", dpi=130, bbox_inches="tight")
plt.close(fig)

# Data story (numbers are calculated from the data)
top = df["rating"].value_counts().idxmax()
avg_by_rating = df.groupby("rating")["price_gbp"].mean()
corr = df["price_gbp"].corr(df["rating"], method="spearman")
band = df["price_band"].value_counts().idxmax()
high = (df["rating"] >= 4).mean() * 100

story = f"""# Data Story: What do 1,000 books tell us?

**Overview.** The dataset has {len(df)} books priced between £{df.price_gbp.min():.2f}
and £{df.price_gbp.max():.2f}, with an average of £{df.price_gbp.mean():.2f}.

**Insight 1: Ratings.** The most common rating is {top} stars, and {high:.0f}% of books
are rated 4 stars or higher (see chart_ratings.png).

**Insight 2: Prices.** Most books fall in the £{band} price band
(see chart_prices.png and chart_heatmap.png).

**Insight 3: Price vs rating.** Average price ranges only from £{avg_by_rating.min():.2f}
to £{avg_by_rating.max():.2f} across ratings. The correlation is {corr:.2f}, so a higher
price does not mean a better rating (see chart_price_by_rating.png).

**Decision support.** Buyers should not use price as a sign of quality, and sellers
cannot expect to charge more just because a book is rated higher.
"""
with open("data_story.md", "w") as f:
    f.write(story)
print("Saved 4 charts, dashboard.png and data_story.md")