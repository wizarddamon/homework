import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import re
import numpy as np


data_path = 'ufo_sightings_scrubbed.csv'
df = pd.read_csv(data_path, low_memory=False)

df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
df['date posted'] = pd.to_datetime(df['date posted'], errors='coerce')
df['year'] = df['datetime'].dt.year

df['duration (seconds)'] = pd.to_numeric(df['duration (seconds)'], errors='coerce')
df = df.dropna(subset=['duration (seconds)'])

plt.figure(figsize=(12, 6))
year_counts = df['year'].value_counts().reset_index()
year_counts.columns = ['year', 'count']

bars = sns.barplot(data=year_counts, x='year', y='count')
plt.title('UFO Sightings by Year')
plt.xlabel('Year')
plt.ylabel('Number of Sightings')
plt.xticks(rotation=90)

cmap = plt.get_cmap('viridis')
colors = cmap(np.linspace(0, 1, len(year_counts)))
for bar, color in zip(bars.containers[0], colors):
    bar.set_facecolor(color)
plt.show()

plt.figure(figsize=(12, 6))
shape_counts = df['shape'].value_counts().reset_index()[:10]
shape_counts.columns = ['shape', 'count']

bars = sns.barplot(data=shape_counts, y='shape', x='count')
plt.title('Top 10 UFO Shapes by Sightings')
plt.xlabel('Number of Sightings')
plt.ylabel('Shape')

colors = cmap(np.linspace(0, 1, len(shape_counts)))
for bar, color in zip(bars.containers[0], colors):
    bar.set_facecolor(color)
plt.show()

if 'comments' in df.columns:
    stopwords = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
                 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
                 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that',
                 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
                 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as',
                 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
                 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off',
                 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how',
                 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not',
                 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should',
                 'now'}

    def clean_text(text):
        text = text.lower()
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        words = text.split()
        words = [word for word in words if word not in stopwords]
        return ' '.join(words)

    df['cleaned_comments'] = df['comments'].dropna().apply(clean_text)
    df['cleaned_comments'] = df['cleaned_comments'].astype(str)
    all_comments = ' '.join(df['cleaned_comments'])

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_comments)
    plt.figure(figsize=(12, 8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of UFO Sightings Comments')
    plt.show()
else:
    print("Warning: 'comments' column not found. Skipping text analysis.")