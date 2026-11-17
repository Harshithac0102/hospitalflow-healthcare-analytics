from pathlib import Path
import streamlit as st
import plotly.express as px
from hospitalflow.analytics import load_data, summary, hourly_pattern

st.set_page_config(page_title='HospitalFlow | ED Analytics',layout='wide')
st.title('HospitalFlow | Emergency Department Analytics')
st.caption('Exploratory analysis of a Kaggle patient-flow dataset. Not for clinical use.')
source = Path('data/healthcare_analytics_patient_flow_data.csv')
if not source.exists():
    st.error('Dataset not found. Put healthcare_analytics_patient_flow_data.csv inside the data folder.')
    st.stop()
@st.cache_data
def get_data():
    return load_data(source)
df = get_data()
st.sidebar.header('Explore visits')
selected = st.sidebar.multiselect('Referral department', sorted(df.referral.unique()),default=sorted(df.referral.unique()))
filtered = df[df.referral.isin(selected)]
if filtered.empty:
    st.warning('Select at least one referral department.')
    st.stop()
s = summary(filtered)
a,b,c,d = st.columns(4)
a.metric('Visits',f"{s['visits']:,}")
b.metric('Average wait',f"{s['mean_wait']} min")
c.metric('90th percentile wait',f"{s['p90_wait']} min")
d.metric('Admission rate',f"{s['admission_rate']}%")
left,right=st.columns(2)
with left:
    st.plotly_chart(px.histogram(filtered,x='wait_minutes',nbins=30,title='Waiting-time distribution',labels={'wait_minutes':'Wait (minutes)'}),use_container_width=True)
    st.plotly_chart(px.bar(filtered.groupby('referral',as_index=False).agg(visits=('patient_id','size')).sort_values('visits',ascending=False),x='referral',y='visits',title='Visits by referral department'),use_container_width=True)
with right:
    st.plotly_chart(px.line(hourly_pattern(filtered),x='hour',y='visits',markers=True,title='Recorded arrival hour'),use_container_width=True)
    st.plotly_chart(px.box(filtered,x='admission_flag',y='wait_minutes',title='Wait time by admission status'),use_container_width=True)
st.subheader('Data quality and interpretation')
st.write(f"Missing satisfaction scores: **{s['missing_satisfaction']:,}** of {s['visits']:,} filtered records.")
st.write(f"Ambiguous day/month dates: **{s['ambiguous_dates']:,}**. The loader assumes month-first when both date components are 12 or less; validate with the dataset author before relying on calendar trends.")
st.info('Wait times and admission flags are recorded values. This dataset does not establish staffing, bed availability, clinical outcomes, or causal effects. No patient-flow simulation is included in this version.')
with st.expander('View cleaned sample'):
    st.dataframe(filtered[['date_raw','hour','age','gender','referral','admission_flag','wait_minutes','satisfaction']].head(50),use_container_width=True)
