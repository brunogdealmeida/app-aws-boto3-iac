import streamlit as st
import boto3
from utils.utils_s3 import S3Manager

s3 = boto3.Session(profile_name='default').client('s3')
s3_manager = S3Manager(s3)

def siderbar():
    # Set siderbar menu
    st.sidebar.title("Menu")

    # Define as opções do menu
    pages = ['Home','Upload no S3', 'Download do S3']

    # Define a página atual a partir da seleção do menu
    page = st.sidebar.radio('Selecione o que deseja fazer', pages)

    # Mostra a página atual e oculta a página padrão, se necessário
    if page == 'Home':
        app_home()
    elif page == 'Upload no S3':
        app_upload()
    elif page == 'Download do S3':
        app_download()
    else:
        app_home()

def app_home():
    st.title('Seja Bem-Vindo')
    st.write('Esse app tem como objetivo o aprendizado de provisionamento de recursos na AWS.')

# Create a Streamlit app
def app_upload():
    st.title('Upload file to S3')

    # User select the name of the bucket
    bucket_name = st.selectbox('Selecione o bucket que deseja inserir o arquivo:',(s3_manager.list_buckets()))

    # Allow user to upload a file
    file = st.file_uploader('Select a file')

    # Display a preview of the uploaded file
    if file is not None:
        st.write('Preview:')
        st.write(file.read())

    # User to confirm upload
    if st.button('Upload'):
        # Check if the bucket name is valid
        if bucket_name is None:
            st.error('Please enter a valid bucket name.')
        else:
            # Try Upload the file to S3
            try:
                s3.upload_fileobj(file, bucket_name, file.name)
                st.success(f'File uploaded to {bucket_name}!')
            except Exception as e:
                st.error(f'Error uploading file: {e}')

def app_download():
    st.title('Download de arquivos do S3')
    st.write('Aqui você consegue baixar os arquivos do seu bucket.')

# Run the app
if __name__ == '__main__':
    siderbar()
    
