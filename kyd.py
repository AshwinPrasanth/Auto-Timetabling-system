import streamlit as st
import pandas as pd
import random
import matplotlib.pyplot as plt
import numpy as np

class Edaboost:
    def __init__(self, csv_path):
        self.df = pd.read_csv(csv_path)
        self.model = 1
        self.tokenizer = 2

    def query(self, prompt):
        x = np.arange(10)
        s = x.mean()
        y = np.random.randint(1, 20, size=10)
        fig, ax = plt.subplots()
        ax.bar(x, y)
        random_choice = random.choice([1, 2])
        if random_choice == 1:
            return s, True
        else:
            return fig, False

def main():
    st.title("EDA Boost")

    # Positioning the image in the top-left corner using CSS
    st.markdown(
        """
        <style>
            .top-left {
                position: absolute;
                top: -150px;
                left: -460px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="top-left">
            <img src="white.png" width="250">
        </div>
        """,
        unsafe_allow_html=True
    )

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file is not None:
        eda = Edaboost(uploaded_file)

        st.write("CSV File Uploaded Successfully!")

        prompt = st.text_input("Type something:")

        if prompt:
            result, is_numerical = eda.query(prompt)

            if is_numerical:
                st.write("Numerical Result:")
                st.write(result)
            else:
                st.write("Image Result:")
                st.pyplot(result)

if __name__ == "__main__":
    main()
