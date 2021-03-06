from keras.datasets import cifar10
from sklearn import svm
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
import pickle

with open('/home/agnieszka/codes_train.pkl', 'rb') as codes:
    codes_train = pickle.load(codes)

with open('/home/agnieszka/codes_test.pkl', 'rb') as codes:
    codes_test = pickle.load(codes)

(_, y_train), (_, y_test) = cifar10.load_data()

param_grid = [{'model__kernel': ['linear'], 'model__C': [0.001, 0.01, 0.1, 1]},
              {'model__kernel': ['rbf'], 'model__C': [0.01, 0.1, 1, 10, 100], 'model__gamma':[1e-6, 1e-5, 1e-4, 'scale']}]

pipe = Pipeline([('scaler', StandardScaler()), ('model', svm.SVC())])

gs = GridSearchCV(pipe, param_grid, cv=3, n_jobs=-1, verbose=10, return_train_score=True)
gs.fit(codes_train, y_train.flatten())
print('Best parameters:', gs.best_params_)

best_model_st = gs.best_estimator_

with open('/home/agnieszka/best_model_st.sav', 'wb') as model:
    pickle.dump(best_model_st, model)

pred_1 = best_model_st.predict(codes_test)
pred_2 = best_model_st.predict(codes_train)

print('Accuracy on test set:', accuracy_score(pred_1, y_test.flatten()))
print('Accuracy on train set:', accuracy_score(pred_2, y_train.flatten()))

