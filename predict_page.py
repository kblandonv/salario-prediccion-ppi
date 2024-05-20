import streamlit as st
import pickle
import numpy as np


def load_model():
    """
    This function loads a pre-trained model from a file named 'saved_steps.pkl'.
    
    It opens the file in read-binary mode ('rb') and uses the pickle module's load function to deserialize the data from the file.
    
    The deserialized data is returned by the function. This data typically includes the pre-trained model and any other necessary preprocessing steps that were saved along with the model.

    Returns:
    data: The deserialized data from the 'saved_steps.pkl' file, typically including a pre-trained model and preprocessing steps.
    """

    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    """
    This function displays a prediction page for Software Developer Salaries using a pre-trained model.
    
    It first sets the title of the page and provides a brief introduction.
    
    It then asks the user to provide some information, including their country, education level, and years of experience. The user inputs their country and education level from predefined lists using select boxes, and their years of experience using a slider.
    
    The user then clicks a button to calculate their predicted salary. If the button is clicked, the function prepares the input data, transforms it using pre-trained label encoders, and feeds it into the pre-trained model to get the predicted salary.
    
    Finally, the function displays the predicted salary on the page.
    """
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = (
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    )

    education = (
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    )

    country = st.selectbox("Country", countries)
    education = st.selectbox("Education Level", education)

    expericence = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = np.array([[country, education, expericence ]])
        X[:, 0] = le_country.transform(X[:,0])
        X[:, 1] = le_education.transform(X[:,1])
        X = X.astype(float)

        salary = regressor.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
