import pandas as pd
df = pd.read_csv('labels.csv')
print("Total rows:", len(df))
print("Unique texts:", df['text'].nunique())
dupes = df[df.duplicated(subset='text', keep=False)].sort_values('text')
if len(dupes) > 0:
    print(f"\n{len(dupes)} rows involved in duplicates:\n")
    for text in dupes['text'].unique():
        print(f"- {text[:80]}...")
else:
    print("\nNo duplicates found.")
print("\nLabel counts:")
print(df['label'].value_counts())