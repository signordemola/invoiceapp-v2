

import os 
import json
from jinja2 import Environment, FileSystemLoader


from applib.lib.helper import (
    send_email_postmark, set_email_read_feedback,
    attach_functn, generate_html_template
)



def main() -> None:

    with open('./contacts.txt') as fl:        
        contacts = json.loads(fl.read())

    contacts.append(
        {'email': 'dharmielola@gmail.com', 'name': 'Creative Pluck'}
    )

    
    message_subject = 'Happy Yuletides'
    # email = 'jeffdico@gmail.com'
    # receiver_email = 'jeffrey@ecardex.com'
    

    for contact in contacts:       

        status_link = set_email_read_feedback(
            view=0,
            email_receiver=contact['email'], ref_id=3,
            ref_type='broadcast',
            email_title=message_subject
        ) 
         
        template = generate_html_template(
            'invoice_template', 'celebratory.html',
            name=contact['name'],  status_link=status_link             
        )

        with open('invoice_template/banner.jpeg', 'rb') as fl:

            send_email_postmark(contact['email'], message_subject, template,            
                attachment_content=fl.read(), attachment_name='happyyultide.jpeg'
            )

 


if __name__ == '__main__':
    main()