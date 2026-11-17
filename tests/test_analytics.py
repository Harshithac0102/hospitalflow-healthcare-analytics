import pandas as pd
from hospitalflow.analytics import load_data, summary

def test_load_and_summary(tmp_path):
    df=pd.DataFrame([{'Patient Id':'a','Patient Admission Date':'15/09/2023','Patient Admission Time':'9:25:00 AM','Patient Gender':'Female','Patient Age':33,'Patient Race':'Other','Department Referral':None,'Patient Admission Flag':'Admission','Patient Satisfaction Score':None,'Patient Waittime':20}])
    p=tmp_path/'example.csv'; df.to_csv(p,index=False)
    result=load_data(p)
    assert result.loc[0,'date'].strftime('%Y-%m-%d')=='2023-09-15'
    assert result.loc[0,'referral']=='Not recorded'
    assert summary(result)['admission_rate']==100.0

def test_missing_columns(tmp_path):
    p=tmp_path/'bad.csv'; pd.DataFrame({'foo':[1]}).to_csv(p,index=False)
    try:
        load_data(p)
    except ValueError as exc:
        assert 'Missing required columns' in str(exc)
    else:
        raise AssertionError('Expected validation error')
