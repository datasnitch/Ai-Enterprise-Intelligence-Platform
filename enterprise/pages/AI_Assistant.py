import streamlit as st

from enterprise.ai_engine.decision_engine import ask_business_ai


def ai_page():

    st.title("🤖 AI Business Assistant")

    st.markdown("""
Ask questions about your enterprise data.

### Example Questions

- Which product generated the highest sales?
- Which city has the most customers?
- Show the top performing products.
- Which category is most profitable?
- Give recommendations to increase revenue.
- Analyze current business performance.
""")

    question = st.text_area(
        "Business Question",
        height=150,
        placeholder="Example: Which products generated the highest revenue?"
    )

    if st.button("🚀 Ask AI", use_container_width=True):

        if question.strip() == "":
            st.warning("Please enter a business question.")
            st.stop()

        with st.spinner("AI is analyzing your business data..."):

            try:

                answer = ask_business_ai(question)

                st.success("Analysis Complete")

                st.markdown(answer)

            except Exception as e:

                st.error(f"Error: {e}")