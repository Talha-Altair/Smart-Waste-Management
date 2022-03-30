import streamlit as st
import streamlit_authenticator as stauth
import main
import warnings
warnings.simplefilter('ignore')


names = ['Rohith','Adithya']
usernames = ['rohith','adithya']
passwords = ['123','456']

hashed_passwords = stauth.Hasher(passwords).generate()

authenticator = stauth.Authenticate(names,usernames,hashed_passwords,
    'some_cookie_name','some_signature_key',cookie_expiry_days=0)

name, authentication_status, usernames = authenticator.login('Login','main')

if authentication_status:
    st.write('Welcome *%s*' % (name))
    page = main
    page.app()

elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.error('Please enter your username and password',)
