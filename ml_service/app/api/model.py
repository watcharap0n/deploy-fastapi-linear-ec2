import numpy as np
from fastapi import APIRouter
from sklearn.linear_model import LinearRegression
from app.schema.model import Prediction

router = APIRouter()

raw_data = [[3, 10],  # simple data negative
            [5, 7],
            [6, 6],
            [7, 4.5],
            [9, 3.5]]


@router.get('/linear/data')
async def simple_data():
    return np.array(raw_data)


async def loop_variable_value(x_pred, y_pred):
    lst = []
    for k, v in enumerate(x_pred):
        value = {'x': f'{v[0]}', 'y': f'{y_pred[k].round(2)}'}
        lst.append(value)
    return lst


@router.post('/linear/prediction', summary='Prediction Model Simple Linear')
async def prediction(payload: Prediction):
    data = np.array(raw_data)
    x = data[:, 0].reshape(-1, 1)
    y = data[:, 1]
    clf = LinearRegression()
    clf.fit(x, y)
    x_pred = np.array(payload.x_predict).reshape(-1, 1)
    y_pred = clf.predict(x_pred)
    lst = await loop_variable_value(x_pred, y_pred)
    return lst
