import streamlit as st
import pickle as pk
import numpy as np
import warnings

warnings.filterwarnings("ignore")

# Load the model
try:
    loaded_model = pk.load(open('crop.sav', 'rb'))
except FileNotFoundError:
    st.error("Model file 'crop.sav' not found.")
    st.stop()
except Exception as e:
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

# Crop dictionary mapping the index to a descriptive message
crop_dict = {
    0: 'Apple',
    1: 'Banana',
    2: 'Blackgram',
    3: 'Chickpea',
    4: 'Coconut',
    5: 'Coffee',
    6: 'Cotton',
    7: 'Grapes',
    8: 'Jute',
    9: 'Kidneybeans',
    10: 'Lentil',
    11: 'Maize',
    12: 'Mango',
    13: 'Mothbeans',
    14: 'Mungbean',
    15: 'Muskmelon',
    16: 'Orange',
    17: 'Papaya',
    18: 'Pigeonpeas',
    19: 'Pomegranate',
    20: 'Rice',
    21: 'Watermelon'
}

def get_recommendation(input_data):
    try:
        array_input = np.array(input_data)
        reshaped_input = array_input.reshape(1, -1)
        prediction = loaded_model.predict(reshaped_input)
        return prediction[0]  # Return the prediction index
    except Exception as e:
        st.error(f"An error occurred while making the prediction: {e}")
        return None

def main():
    st.markdown("<h1 style='text-decoration: underline; color: DarkGreen;'>Crop Recommendation System 🌱</h1>", unsafe_allow_html=True)

    # Adding a background image with transparency
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(rgba(255, 255, 255, 0.5), rgba(255, 255, 255, 0.5)), 
            url("https://i.postimg.cc/fWKG7DBH/th-3.jpg");
            background-size: cover;
        }
        .center-button {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px; /* Add some margin for spacing */
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            padding: 15px;
            background: #000; /* Black background for the card */
            color: #fff; /* White text color for contrast */
            max-width: 300px;
            margin: 0 auto;
            text-align: center;
        }
        .card img {
            width: 70px;
            height: 70px;
            object-fit: cover;
            border-radius: 50%;
        }
        .tooltip {
            display: inline-block;
            position: relative;
        }
        .tooltip .tooltiptext {
            visibility: hidden;
            width: 160px;
            background-color: #555;
            color: #fff;
            text-align: center;
            border-radius: 6px;
            padding: 5px 0;
            position: absolute;
            z-index: 1;
            bottom: 125%;
            left: 50%;
            margin-left: -80px;
            opacity: 0;
            transition: opacity 0.3s;
        }
        .tooltip:hover .tooltiptext {
            visibility: visible;
            opacity: 1;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Input fields in columns with tooltips
    col1, col2, col3 = st.columns(3)

    with col1:
        N = st.number_input("**Nitrogen (N) in soil**", help="Enter the Nitrogen content in soil in kg/ha")

    with col2:
        P = st.number_input("**Phosphorus (P) in soil**", help="Enter the Phosphorus content in soil in kg/ha")

    with col3:
        K = st.number_input("**Potassium (K) in soil**", help="Enter the Potassium content in soil in kg/ha")

    with col1:
        temperature = st.number_input("**Temperature** (°C) of soil", help="Enter the temperature in degrees Celsius")

    with col2:
        humidity = st.number_input("**Humidity** (%) of soil", help="Enter the soil humidity percentage")

    with col3:
        ph = st.number_input("**pH**", help="Enter the pH level of the soil")

    rainfall = st.number_input("**Rainfall** (mm)", help="Enter the total rainfall in millimeters")

    # Centering the button
    st.markdown('<div class="center-button">', unsafe_allow_html=True)
    if st.button("**Get Crop Recommendation**"):
        # Validate inputs
        if all(v >= 0 for v in [N, P, K, temperature, humidity, ph, rainfall]):
            # Prepare input for the model
            input_data = [N, P, K, temperature, humidity, ph, rainfall]

            # Get the recommended crop index
            pred_index = get_recommendation(input_data)

            # Check if the prediction index is in the crop dictionary
            if pred_index is not None and pred_index in crop_dict:
                crop = crop_dict[pred_index]
                result = f"{crop} is the best crop to be cultivated right there."
                
                # Display the result in a card format
                st.markdown(
                    f"""
                    <div class="card">
                      <img src="https://i.postimg.cc/pTxW0v4s/crop.png" class="card-img-top" alt="Crop Image">
                      <div class="card-body">
                        <h5 class="card-title" style="color: #fff; font-weight: bold;">Recommended Crop for Cultivation:</h5>
                        <p class="card-text" style="color: #fff; font-weight: bold;">{result}</p>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                st.balloons()
            else:
                st.markdown("<h3 style='color: red;'><b>Crop recommendation could not be determined.</b></h3>", unsafe_allow_html=True)
        else:
            st.markdown("<h3 style='color: red;'><b>Please enter valid values for all inputs.</b></h3>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
