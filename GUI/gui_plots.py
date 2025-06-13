import streamlit as st
import pandas as pd
from src.scheduler.fitness import fitness

def display_schedule(schedule, idx, title="Schedule"):
    penalty = fitness(schedule)
    schedule_data = [[
        match[0],
        match[1],
        match[2],
        match[3],
        match[4],
        match[5]
    ]for match in schedule]

    schedule_df = pd.DataFrame(schedule_data)
    st.subheader(f"{title} {idx + 1}")
    st.dataframe(schedule_df)
    st.write(f"Penalty: {penalty}")
