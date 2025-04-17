import streamlit as st


def main():
    st.set_page_config(
        page_title="NBA Shot Chart Analyzer",
        page_icon="🏀",
        layout="wide",
    )

    st.title("NBA Shot Chart Analyzer")
    st.write(
        "Welcome to the NBA Shot Chart Analyzer. This application allows you to visualize shooting patterns of NBA players."  # noqa: E501
    )

    # プレースホルダー
    st.info("This application is currently under development.")


if __name__ == "__main__":
    main()
