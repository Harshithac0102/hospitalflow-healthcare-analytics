from pathlib import Path
import pandas as pd

REQUIRED = {'Patient Id','Patient Admission Date','Patient Admission Time','Patient Gender','Patient Age','Patient Race','Department Referral','Patient Admission Flag','Patient Satisfaction Score','Patient Waittime'}

def load_data(path):
    df = pd.read_csv(Path(path))
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f'Missing required columns: {sorted(missing)}')
    df = df.rename(columns={
        'Patient Id':'patient_id','Patient Admission Date':'date_raw',
        'Patient Admission Time':'time_raw','Patient Gender':'gender',
        'Patient Age':'age','Patient Race':'race','Department Referral':'referral',
        'Patient Admission Flag':'admission_flag',
        'Patient Satisfaction Score':'satisfaction','Patient Waittime':'wait_minutes'})
    # Source has mixed DD/MM/YYYY and MM/DD/YYYY strings. Unambiguous dates
    # are parsed using the only possible ordering; ambiguous dates default to
    # month-first and are flagged for transparency.
    pieces = df['date_raw'].astype(str).str.split('/', expand=True)
    a = pd.to_numeric(pieces[0], errors='coerce')
    b = pd.to_numeric(pieces[1], errors='coerce')
    df['ambiguous_date'] = (a <= 12) & (b <= 12)
    dayfirst = a > 12
    normalized = df['date_raw'].where(~dayfirst, pieces[1]+'/'+pieces[0]+'/'+pieces[2])
    df['date'] = pd.to_datetime(normalized, format='%m/%d/%Y', errors='coerce')
    df['hour'] = pd.to_datetime(df['time_raw'], format='%I:%M:%S %p', errors='coerce').dt.hour
    df['referral'] = df['referral'].fillna('Not recorded')
    df['admitted'] = df['admission_flag'].eq('Admission')
    df['wait_minutes'] = pd.to_numeric(df['wait_minutes'], errors='coerce')
    return df

def summary(df):
    return {'visits':len(df),'mean_wait':round(df['wait_minutes'].mean(),1),
            'p90_wait':round(df['wait_minutes'].quantile(.9),1),
            'admission_rate':round(100*df['admitted'].mean(),1),
            'missing_satisfaction':int(df['satisfaction'].isna().sum()),
            'ambiguous_dates':int(df['ambiguous_date'].sum())}

def hourly_pattern(df):
    return df.groupby('hour',as_index=False).agg(visits=('patient_id','size'),mean_wait=('wait_minutes','mean'))
