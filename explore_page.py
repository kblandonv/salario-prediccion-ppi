import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def shorten_categories(categories, cutoff):
    """
    This function takes a pandas Series 'categories' and a 'cutoff' value as input. 
    It iterates over the 'categories' Series, and for each category, if its value is greater than or equal to 'cutoff', 
    it maps the category to itself in 'categorical_map'. 
    If the category's value is less than 'cutoff', it maps the category to 'Other' in 'categorical_map'.
    Finally, it returns the 'categorical_map' dictionary.

    Parameters:
    categories (pd.Series): A pandas Series where the index represents category names and the values represent category counts.
    cutoff (int): The threshold value for determining if a category should be mapped to 'Other'.

    Returns:
    categorical_map (dict): A dictionary where the keys are the original category names and the values are either the original category names (if the category count was >= cutoff) or 'Other' (if the category count was < cutoff).
    """
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map


def clean_experience(x):
    """
    Clean the input experience value to ensure consistency and numerical representation.

    Parameters:
    x (str or int): The input experience value to be cleaned.

    Returns:
    float: The cleaned numerical representation of the experience value.

    Example:
    clean_experience('More than 50 years') -> 50.0
    clean_experience('Less than 1 year') -> 0.5
    clean_experience(5) -> 5.0
    """
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    """
    This function takes a string 'x' as input, which represents a person's highest level of education. 
    It checks if certain key phrases are in 'x', and returns a simplified version of the person's education level based on these checks.
    If 'x' contains 'Bachelor’s degree', it returns 'Bachelor’s degree'.
    If 'x' contains 'Master’s degree', it returns 'Master’s degree'.
    If 'x' contains 'Professional degree' or 'Other doctoral', it returns 'Post grad'.
    If 'x' does not contain any of the above phrases, it returns 'Less than a Bachelors'.

    Parameters:
    x (str): A string representing a person's highest level of education.

    Returns:
    str: A simplified version of the person's education level.
    """
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    """
    This function loads a CSV file named 'survey_results_public.csv' into a pandas DataFrame 'df'. 
    It then performs several cleaning and filtering operations on 'df':
    - It keeps only the columns "Country", "EdLevel", "YearsCodePro", "Employment", and "ConvertedComp".
    - It removes rows where "ConvertedComp" is null.
    - It removes any remaining rows with null values.
    - It keeps only the rows where "Employment" is "Employed full-time", and then drops the "Employment" column.
    - It applies the 'shorten_categories' function to the "Country" column, which maps less frequent countries to 'Other'.
    - It filters out rows where "ConvertedComp" is not between 10,000 and 250,000.
    - It removes rows where "Country" is 'Other'.
    - It applies the 'clean_experience' function to the "YearsCodePro" column and the 'clean_education' function to the "EdLevel" column.
    - It renames the "ConvertedComp" column to "Salary".
    Finally, it returns the cleaned and filtered DataFrame.

    Returns:
    df (pd.DataFrame): The cleaned and filtered DataFrame.
    """
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed full-time"]
    df = df.drop("Employment", axis=1)

    country_map = shorten_categories(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(clean_experience)
    df["EdLevel"] = df["EdLevel"].apply(clean_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    """
    This function displays an exploration page for Software Engineer Salaries using data from the Stack Overflow Developer Survey 2020.
    
    It first sets the title of the page and provides a brief introduction.
    
    It then creates a pie chart showing the distribution of data across different countries. The pie chart is drawn as a circle due to the equal aspect ratio.
    
    Next, it displays the mean salary based on country in a bar chart. The data is grouped by country and the mean salary is calculated for each group. The data is sorted in ascending order before being displayed.
    
    Finally, it displays the mean salary based on experience in a line chart. The data is grouped by years of professional coding experience and the mean salary is calculated for each group. The data is sorted in ascending order before being displayed.
    """
    
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    data = df["Country"].value_counts()

    fig1, ax1 = plt.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.write("""#### Number of Data from different countries""")

    st.pyplot(fig1)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)

