import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression



def text_fit(X, y, model,clf_model,coef_show=1):   
    X_c = model.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_c, y, random_state=42)
    clf = clf_model.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)
    print ('Model Accuracy: {}'.format(acc))
    

data = pd.read_csv('Finland_Hotels_Reviews.csv')
newData = data.loc[:,['review', 'rating','review_title']]
X= newData['review'].fillna(newData['review_title'])
y_dict = {1:0, 2:0,3:1,  4:1, 5:1}
y = newData['rating'].map(y_dict)



tfidf = TfidfVectorizer(stop_words = 'english')
text_fit(X, y, tfidf, LogisticRegression())