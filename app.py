# Save this as app.py and run using: streamlit run app.py

import streamlit as st
import matplotlib.pyplot as plt

# Constants
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
DAILY_GOAL = 14  # cups
WEEKLY_GOAL = 70  # cups
POOL_CAPACITY = 30000  # gallons
GALLONS_PER_CUP = 428.6

# Session state to persist data
if 'intake' not in st.session_state:
    st.session_state.intake = {day: 0 for day in DAYS}
if 'current_day_index' not in st.session_state:
    st.session_state.current_day_index = 0

st.title("🏊 Water Intake Tracker (Web Version)")
st.subheader("Track your hydration and fill your virtual swimming pool!")

day_index = st.session_state.current_day_index

if day_index < len(DAYS):
    day = DAYS[day_index]
    st.write(f"### Enter your water intake for **{day}** (in cups):")
    cups = st.number_input("Cups:", min_value=0.0, step=0.5, key=day)

    if st.button("Submit"):
        st.session_state.intake[day] = cups
        st.session_state.current_day_index += 1
        st.experimental_rerun()
else:
    st.success("✅ You’ve entered all days of the week!")

# Calculate totals
total_cups = sum(st.session_state.intake.values())
total_gallons = total_cups * GALLONS_PER_CUP
remaining_gallons = max(POOL_CAPACITY - total_gallons, 0)

# Summary
st.write("## 📊 Weekly Summary")
for day, cups in st.session_state.intake.items():
    status = "✅ Goal met!" if cups >= DAILY_GOAL else f"⚠️ {DAILY_GOAL - cups:.1f} cups short"
    st.write(f"- **{day}:** {cups} cups ({status})")

st.write(f"**Total Cups Drank:** {total_cups}")
st.write(f"**Total Gallons Added to Pool:** {total_gallons:.1f}")
st.write(f"**Gallons Remaining to Fill Pool (30,000 gal):** {remaining_gallons:.1f}")

# Visual pool fill
st.write("## 🖼️ Pool Fill Visualization")
fill_ratio = min(total_gallons / POOL_CAPACITY, 1.0)

fig, ax = plt.subplots(figsize=(6, 2))
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.add_patch(plt.Rectangle((0.05, 0.1), 0.9, 0.5, edgecolor='black', facecolor='lightblue'))
ax.add_patch(plt.Rectangle((0.05, 0.1), 0.9 * fill_ratio, 0.5, facecolor='blue'))
ax.text(0.5, 0.7, f"{total_gallons:.1f} gal filled", ha='center', fontsize=12)
ax.axis('off')
st.pyplot(fig)

# Final status
if total_cups >= WEEKLY_GOAL:
    st.balloons()
    st.success("🎉 You met your weekly goal of 70 cups!")
else:
    st.info(f"You're {WEEKLY_GOAL - total_cups:.1f} cups away from your weekly goal.")
