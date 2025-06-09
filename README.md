# 🧠 Article Insight Engine

A Python-based tool that scrapes online articles, performs Natural Language Processing (NLP), and generates a comprehensive sentiment and readability analysis report in Excel format.

## 📌 Features

- ✅ Web scraping of article content from provided URLs
- ✅ Text cleaning and parsing with `BeautifulSoup`
- ✅ Sentiment analysis using `TextBlob` and custom dictionaries
- ✅ Readability metrics: FOG Index, Complex Words %, Avg Sentence Length, etc.
- ✅ Output results to `Output Data Structure.xlsx`
- ✅ Modular and easy to extend



This will:

* Scrape content from URLs in `Input.xlsx`
* Analyze each article
* Save results in `Output Data Structure.xlsx`

---

## 📊 Output Metrics

Each article is evaluated on:

* Positive Score
* Negative Score
* Polarity & Subjectivity
* Average Sentence Length
* % of Complex Words
* FOG Index
* Personal Pronoun Count
* Word Count, Syllable Count, Word Length, and more

---

## 🔧 Requirements

```text
requests
beautifulsoup4
textblob
nltk
pandas>=1.0
openpyxl>=3.0
```

