import streamlit as st
import base64
import sklearn
import numpy as np
import pickle as pkl
from sklearn.preprocessing import MinMaxScaler
scal=MinMaxScaler()
#Load the saved model
model=pkl.load(open("final_model.p","rb"))




st.set_page_config(page_title="Predicting Distant Metastasis in Neuroblastoma",
                   page_icon="⚕️",layout="centered",initial_sidebar_state="expanded")



def preprocess(Chemotherapy,Grade,Radiation,Tumor_Primary_Site,Regional_Lymph_Nodes,Surgery_Type):   
 
    
    # Pre-processing user input   
    if Chemotherapy=="Yes":
        Chemotherapy=1 
    else: Chemotherapy=0
    
    if Grade=="I-II":
        Grade=1
    elif Grade=="III":
        Grade=2
    elif Grade=="IV":
        Grade=3
    elif Grade=="Unknown":
        Grade=4
    
    if Radiation=="Yes":
        Radiation=1
    elif Radiation=="No":
        Radiation=0
 
    if Tumor_Primary_Site=="Adrenal gland":
        Tumor_Primary_Site=1
    elif Tumor_Primary_Site=="Retroperitoneum":
          Tumor_Primary_Site=2
    elif Tumor_Primary_Site=="Other":
        Tumor_Primary_Site=3  
 
    if Regional_Lymph_Nodes=="No nodes were examined":
        Regional_Lymph_Nodes=0
    elif Regional_Lymph_Nodes=="Negative":
        Regional_Lymph_Nodes=1
    elif Regional_Lymph_Nodes=="Positive":
        Regional_Lymph_Nodes=2
    elif Regional_Lymph_Nodes=="Unknown":
        Regional_Lymph_Nodes=3

    if Surgery_Type=="No Surgery":
        Surgery_Type=0
    elif Surgery_Type=="Local tumor destruction/excision":
        Surgery_Type=1
    elif Surgery_Type=="Partial surgical removal of primary site":
        Surgery_Type=2
    elif Surgery_Type=="Total surgical removal of primary site":
        Surgery_Type=3
        


    user_input=[Chemotherapy,Grade,Radiation,Tumor_Primary_Site,Regional_Lymph_Nodes,Surgery_Type]
    user_input=np.array(user_input)
    user_input=user_input.reshape(1,-1)
    # user_input=scal.fit_transform(user_input)
    prediction=model.predict(user_input)

    return prediction

    
       
    # front end elements of the web page 
html_temp = """ 
    <div style ="background-color:pink;padding:13px"> 
    <h1 style ="color:black;text-align:center;">Predicting Distant Metastasis in Neuroblastoma</h1> 
    </div> 
    """
      
# display the front end aspect
st.markdown(html_temp, unsafe_allow_html = True) 
st.subheader('by Shan Li (*^_^*) ')
      
# following lines create boxes in which user can enter data required to make prediction
# age=st.selectbox ("Age",range(1,121,1))
# oldpeak=st.number_input('Oldpeak')
Chemotherapy=st.radio("Receive Chemotherapy", ['Yes', 'No'])
Grade=st.selectbox('Tumor Grade',("I-II","III","IV","Unknown")) 
Tumor_Primary_Site=st.selectbox('Tumor Primary Site',("Adrenal gland","Retroperitoneum","Other"))
Surgery_Type=st.selectbox('Surgery Type',("No Surgery","Local tumor destruction/excision","Partial surgical removal of primary site","Total surgical removal of primary site"))
Regional_Lymph_Nodes=st.selectbox('Regional Lymph Node Examination',("No nodes were examined","Negative","Positive","Unknown"))
Radiation=st.radio("Receive Radiotherapy", ['Yes','No'])



#user_input=preprocess(Chemotherapy,Grade,Radiation,Tumor_Primary_Site,Regional_Lymph_Nodes,Surgery_Type)
pred=preprocess(Chemotherapy,Grade,Radiation,Tumor_Primary_Site,Regional_Lymph_Nodes,Surgery_Type)



if st.button("Predict"):    
  if pred[0] == 1:
    st.error('Warning! You have high risk of getting distant metastasis!')
    
  else:
    st.success('You have lower risk of getting distant metastasis!')
    
   

st.sidebar.subheader("About App")

st.sidebar.info("This web app is helps you to find out whether you are at a risk of developing distant metastasis for neuroblastoma.")
st.sidebar.info("Enter the required fields and click on the 'Predict' button to check whether you have a risk of getting distant metastasis")
st.sidebar.info("Don't forget to rate this app")



feedback = st.sidebar.slider('How much would you rate this app?',min_value=0,max_value=5,step=1)

if feedback:
  st.header("Thank you for rating the app!")
  st.info("Caution: This is just a prediction and not doctoral advice. Kindly see a doctor in time during the treatment of neuroblastoma.") 
    
