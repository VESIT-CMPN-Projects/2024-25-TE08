import streamlit as st

def show_quiz_page(questions):
    st.title("Quiz Page")
    st.write("Answer the following questions:")

    # Store user answers and submission status in session state
    if "quiz_answers" not in st.session_state:
        st.session_state.quiz_answers = {}
    if "quiz_submitted" not in st.session_state:
        st.session_state.quiz_submitted = {}
    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_correctness" not in st.session_state:
        st.session_state.quiz_correctness = {}

    total_questions = len(questions)

    for i, q in enumerate(questions):
        # Show question with score beside if submitted
        correctness_text = ""
        if f"q{i}" in st.session_state.quiz_submitted:
            if st.session_state.quiz_correctness.get(f"q{i}", False):
                correctness_text = ' <span style="color: green;">(1/1)</span>'  # Green for correct
            else:
                correctness_text = ' <span style="color: red;">(0/1)</span>'  # Red for incorrect

        st.markdown(f"### Q{i + 1}: {q['question']}\n {correctness_text}", unsafe_allow_html=True)

        # Safely get saved answer if any
        saved_answer = st.session_state.quiz_answers.get(f"q{i}")
        index = q["options"].index(saved_answer) if saved_answer in q["options"] else None

        selected_option = st.radio(
            f"Select an answer for Q{i+1}",
            q["options"],
            index=index,
            key=f"q{i}",
            disabled=st.session_state.quiz_submitted.get(f"q{i}", False)
        )

        if st.button(f"Submit Q{i+1}", key=f"submit_q{i}"):
            if selected_option:
                st.session_state.quiz_answers[f"q{i}"] = selected_option
                st.session_state.quiz_submitted[f"q{i}"] = True

                if selected_option == q["correct"]:
                    st.success(f"✅ Correct! {selected_option} is the right answer.")

                    # Display Balloons 🎈
                    st.balloons()

                    # Mark as correct
                    st.session_state.quiz_correctness[f"q{i}"] = True
                    st.session_state.quiz_score += 1

                else:
                    st.error(f"❌ Incorrect! You chose {selected_option}.")
                    st.success(f"✅ Correct Answer: {q['correct']}")
                    # Mark as incorrect
                    st.session_state.quiz_correctness[f"q{i}"] = False
            else:
                st.warning("⚠ Please select an answer before submitting.")

    # After all questions answered
    if all(st.session_state.quiz_submitted.get(f"q{i}", False) for i in range(total_questions)):
        st.success(f"🎉 Quiz Completed! Your Score: {st.session_state.quiz_score}/{total_questions}")

    # Back button to return to the story output page
    if st.button("Back to Story"):
        st.session_state.current_page = "output"
        st.rerun()