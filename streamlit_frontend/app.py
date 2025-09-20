
import streamlit as st
import requests

# Base URL for Django API
API_BASE = 'http://127.0.0.1:8000/api/users'

# Streamlit page config
st.set_page_config(page_title="PetRescue", page_icon="🐶", layout="centered")
st.title('🐾 PetRescue — Frontend')

# Sidebar menu
menu = st.sidebar.selectbox('Menu', ['Register', 'Login', 'Report Pet', 'See Pets'])

# Initialize token in session_state
if 'token' not in st.session_state:
    st.session_state['token'] = None

# ------------------ REGISTER ------------------
if menu == 'Register':
    st.header('Create Account')
    name = st.text_input('Full Name')
    email = st.text_input('Email')
    password = st.text_input('Password', type='password')

    if st.button('Register'):
        if name and email and password:
            resp = requests.post(f'{API_BASE}/register/', json={
                'first_name': name,
                'email': email,
                'password': password
            })
            if resp.status_code == 201:
                try:
                    token = resp.json()['token']
                    st.session_state['token'] = token
                except Exception:
                    token = None
                st.success('Account created successfully!')
            else:
                try:
                    error = resp.json()
                except Exception:
                    error = resp.text
                st.error(f"Error: {error}")
        else:
            st.warning('Please fill all fields.')

# ------------------ LOGIN ------------------
elif menu == 'Login':
    st.header('Login')
    email = st.text_input('Email', key='login_email')
    password = st.text_input('Password', type='password', key='login_password')

    if st.button('Login'):
        if email and password:
            resp = requests.post(f'{API_BASE}/login/', json={
                'email': email,
                'password': password
            })
            if resp.status_code == 200:
                try:
                    token = resp.json()['token']
                    st.session_state['token'] = token
                    st.success('Login successful!')
                except Exception:
                    st.error('Login succeeded but failed to parse token.')
            else:
                try:
                    error = resp.json()
                except Exception:
                    error = resp.text
                st.error(f"Login failed: {error}")
        else:
            st.warning('Please enter email and password.')

# ------------------ REPORT PET ------------------
elif menu == 'Report Pet':
    st.header('Report Lost/Found Pet')

    if st.session_state['token'] is None:
        st.warning('You must login first to report a pet.')
    else:
        name = st.text_input('Pet Name', key='pet_name')
        species = st.selectbox('Species', ['Dog', 'Cat', 'Other'])
        color = st.text_input('Color', key='pet_color')
        age = st.text_input('Age', key='pet_age')
        wound = st.text_input('Wound/Damage', key='pet_wound')
        status = st.selectbox('Status', ['lost', 'found'], key='pet_status')
        image_file = st.file_uploader('Upload Pet Photo', type=['jpg', 'jpeg', 'png'], key='pet_image')

        if st.button('Report Pet'):
            if not name or not species or not color or not age or not status:
                st.warning('Please fill all required fields.')
            else:
                headers = {'Authorization': f'Token {st.session_state["token"]}'}
                data = {
                    'name': name,
                    'species': species,
                    'color': color,
                    'age': age,
                    'wound': wound,
                    'status': status
                }
                files = {}
                if image_file:
                    files['image'] = (image_file.name, image_file.getvalue(), image_file.type)

                resp = requests.post(f'{API_BASE}/pets/', headers=headers, data=data, files=files)

                if resp.status_code in [200, 201]:
                    st.success('Pet reported successfully!')
                else:
                    try:
                        error = resp.json()
                    except Exception:
                        error = resp.text
                    st.error(f"Failed to report pet: {error}")

# ------------------ SEE PETS ------------------
elif menu == 'See Pets':
    st.header('Lost/Found Pets')
    resp = requests.get(f'{API_BASE}/pets/')
    if resp.status_code == 200:
        try:
            pets = resp.json()
        except Exception:
            pets = []
            st.error('Failed to parse pets response.')
        if pets:
            for pet in pets:
                st.subheader(f"{pet['name'] or 'Unknown'} ({pet['status'].capitalize()})")
                st.write(f"Species: {pet['species']}")
                st.write(f"Color: {pet['color']}")
                st.write(f"Age: {pet['age']}")
                st.write(f"Wound: {pet['wound']}")
                if pet.get('image'):
                    st.image(f"http://127.0.0.1:8000{pet['image']}", width=250)
                st.write("---")
        else:
            st.info('No pets found.')
    else:
        st.error('Failed to fetch pets.')
