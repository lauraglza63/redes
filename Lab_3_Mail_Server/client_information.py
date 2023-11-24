from dotenv import load_dotenv
import os

def client_information():
    load_dotenv()
    user_password = os.getenv('GOOGLE_APLICATION_PASSWORD')
    print('Please enter the following information:')
    user_email = input('Your email address: ')
    user_destination_email = input('The destination email: ')
    user_subject = input('Writte the subject: ')
    user_body = input('Writte the message: ')
    return user_email, user_password, user_destination_email, user_subject, user_body