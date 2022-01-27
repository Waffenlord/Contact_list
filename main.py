import json



CONTACT_FILE_PATH = "contacts.json"


def read_contacts(file_path):
    try:
        with open(file_path, 'r') as f:
            contacts = json.load(f)['contacts']
    except FileNotFoundError:
        contacts = []

    return contacts


def write_contacts(file_path, contacts):
    with open(file_path, 'w') as f:
        contacts = {"contacts": contacts}
        json.dump(contacts, f)


def verify_email_address(email):
    if "@" not in email:
        return False

    split_email = email.split("@")
    identifier = "".join(split_email[:-1])
    domain = split_email[-1]

    if len(identifier) < 1:
        return False

    if "." not in domain:
        return False

    split_domain = domain.split(".")

    for section in split_domain:
        if len(section) == 0:
            return False

    return True

def instructions():
    print('''Welcome to your contact list!
The following is a list of useable commands:      
"add": Adds a contact.
"delete": Deletes a contact.
"list": Lists all contacts.
"search": Searches for a contact by name.
"q": Quits the program and saves the contact list.\n''')

def get_action():
    action = ''
    while True:
        action = input('Type a command: ').lower()
        if action not in ['add', 'delete', 'list', 'search', 'q']:
            print('Unknown command.')
        
        else:
            break
    
    return action

def add_contact(contacts):
    new_first = input('First Name: ')
    new_last = input('Last Name: ')
    new_mobile = input('Mobile Phone Number: ')
    new_home_phone = input('Home Phone Number: ')
    new_email = input('Email Address: ')
    new_address = input('Address: ')
    new_dict = dict()

    if len(contacts) > 0:
        for x in contacts:
            if x['first_name'].lower() == new_first.lower() and x['last_name'].lower() == new_last.lower():
                print('A contact with this name already exists.')
                return False
    
    if len(new_first) == 0 or len(new_last) == 0:
        print('New contact must have First and Last name')
        return False

    if len(new_mobile) > 0:
        count = 0
        for num in new_mobile:
            if num.isdigit():
                count += 1
        
        if count != 10:
            print('Invalid mobile phone number.')
            return False
    
    if len(new_home_phone) > 0:
        count = 0
        for num in new_home_phone:
            if num.isdigit():
                count += 1
        
        if count != 10:
            print('Invalid home phone number.')
            return False

    if len(new_email) > 0:
        valid = verify_email_address(new_email)
        if not valid:
            print('Invalid email address')
            return False
    
    new_dict['first_name'] = new_first
    new_dict['last_name'] = new_last
    if len(new_mobile) > 0:
        new_dict['mobile'] = new_mobile
    if len(new_home_phone) > 0:
        new_dict['home_phone'] = new_home_phone
    if len(new_email) > 0:
        new_dict['email'] = new_email
    if len(new_address) > 0:
        new_dict['address'] = new_address
    
    contacts.append(new_dict)
    print('Contact added!')

    return True


def search_for_contact(contacts):
    first_name = input('First name: ').lower()
    last_name = input('Last name: ').lower()
    match = []

    for contact in contacts:
        if len(first_name) > 0 and len(last_name) == 0:
            if contact['first_name'].lower().find(first_name) != -1:
                match.append(contact)
        
        elif len(last_name) > 0 and len(first_name) == 0:
             if contact['last_name'].lower().find(last_name) != -1:
                 match.append(contact)
        
        else:
            if contact['first_name'].lower().find(first_name) != -1 and contact['last_name'].lower().find(last_name) != -1:
                match.append(contact)

    if len(match) < 1:
        print('Found 0 matching contacts')
        return

    print(f'Found {len(match)} matching contacts.')

    list_contacts(match)




def delete_contact(contacts):
    first_name = input('First name: ')
    last_name = input('Last name: ')

    if len(first_name) == 0 or len(last_name) == 0:
        return False

    for contact in contacts:
        if first_name.lower() == contact['first_name'].lower() and last_name.lower() == contact['last_name'].lower():
            answer = input('Are you sure you would like to delete this contact (y/n)? ')
            if answer.lower().startswith('y'):
                contacts.remove(contact)
                print('Contact deleted!')
                return True
            
            else:
                return True
    
    return False



def list_contacts(contacts):
    if len(contacts) < 1:
        print('There are no contacts to show')
        return
    
    contacts.sort(key= lambda x: x['first_name'].lower())

    for c in contacts:
        print(f'{contacts.index(c) + 1}. {c["first_name"].title()} {c["last_name"].title()}')
        if 'mobile' in c:
            print(f'      Mobile: {c["mobile"]}')
        if 'home_phone' in c:
            print(f'      Home: {c["home_phone"]}')
        if 'email' in c:
            print(f'      Email: {c["email"]}')
        if 'address' in c:
            print(f'      Address: {c["address"]}')



def main(contacts_path):
    instructions()
    contacts = read_contacts(contacts_path)
    while True:
        action = get_action()
        if action == 'add':
            successful = add_contact(contacts)
            if not successful:
                print('You entered invalid information, this contact was not added.')
                continue
        
        elif action == 'list':
            list_contacts(contacts)
            continue

        elif action == 'delete':
            delt = delete_contact(contacts)
            if not delt:
                print('No contact with this name exists.')
                continue
        
        elif action == 'search':
            search_for_contact(contacts)
            continue

        elif action == 'q':
            break
    
    write_contacts(contacts_path, contacts)
    if len(contacts) > 0:
        print('Contacts were saved succesfully.')
    
    else:
        print('No contacts were save.')


if __name__ == "__main__":
    main(CONTACT_FILE_PATH)
