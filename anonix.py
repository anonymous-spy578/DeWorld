import os
import json
import uuid
import sys
import shutil
import threading
import time
import random
import smtplib
from email.message import EmailMessage
import textwrap
from textwrap import wrap
from datetime import datetime
import base64
from colorama import Fore, Style, Back, init
init(autoreset=True)

TRANSACTIONS_FILE = 'transactions.json'
SHOP_FILE = 'shop.json'
USERS_FILE = 'users.json'
MESSAGES_FILE = 'messages.json'
GROUPS_FILE = 'groups.json'
FUSERS_FILE = 'fusers.json'
GMESSAGES_FILE = 'gmessages.json'
THEME_FILE = 'theme.json'
    
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def load_json(file):
    if not os.path.exists(file):
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                data = {}
                with open(file, 'w') as f:
                    json.dump(data, f, indent=4)
            return data
    except json.JSONDecodeError:
        with open(file, 'w') as f:
            json.dump({}, f, indent=4)
        return {}

def save_json(file, data):
    try:
        with open(file, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(Fore.RED + f"Failed to save data to {file}: {e}")
        
def loading_az():
    """Display loading animation."""
    animation= ['⌛ loading ..... ','⏳ loading ..... ']*10
    for frame in animation:
        time.sleep(0.3)
        sys.stdout.write("\r" + frame)
        sys.stdout.flush()
        
def refresh():
    """Refresh data from all JSON files to update in-memory data."""
    global groups_data, users_data, messages_data, gmessages_data, fusers_data, shop_data, transactions_data
    groups_data = load_json(GROUPS_FILE)
    messages_data = load_json(MESSAGES_FILE)
    users_data = load_json(USERS_FILE)
    gmessages_data = load_json(GMESSAGES_FILE)
    fusers_data = load_json(FUSERS_FILE)
    shop_data = load_json(SHOP_FILE)
    transactions_data = load_json(TRANSACTIONS_FILE)

def auto_refresh(interval=0.1):
    """Automatically refresh JSON data at a specified interval (in seconds)."""
    while True:
        refresh()
        time.sleep(interval)

def start_auto_refresh(interval=0.1):
    """Start a thread for auto-refreshing."""
    refresh_thread = threading.Thread(target=auto_refresh, args=(interval,))
    refresh_thread.daemon = True
    refresh_thread.start()

def register_user(name, email, password, pin):
    users = load_json(USERS_FILE)
    if email in users:
        print(Fore.RED + "You already have an account.")
        time.sleep(2)
        return None
        
    emojis = ["🧛", "👹", "🤡", "👽", "🤖", "🤑", "😎", "🤓", "🥸", "🤕", "🤠", "👻", "🎃", "😈", "😇", "🤩", "❤️", "😺", "😹", "😿", "😸", "💝", "💓", "💘", "💗", "🫂", "❣️", "💌", "💞", "💀", "👀", "👁️", "🗣️", "🧟", "🧌", "🎄", "🥷", "👼", "💂", "🫅", "🤵", "👰", "🚀", "👷", "👮", "🕵️", "✈️", " 🔬", "⚕️", "🧑", "🏭", "🚒", "🧑🌾", "🏫", "🎓", "🧑‍💼", "⚖️", "🧑‍💻", "🎤", "🎨", "🍳", "👳", "🧕", "👲", "🌻", "🏵️", "🌸", "🥀", "🌹", "💐", "🌍", "🌎", "🐯", "🐼", "🐨", "🐻", "🐶", "🐨", "🐹", "🐭", "🐣", "🐥", "🦭", "🦢", "🦀", "🐋", "🐟", "🐞", "🍑", "🎁", "🎊", "🪩", "💰", "🧸"]     

    user_emoji = random.choice(emojis)
    balance= '0.00'
    username = name.replace(" ", "_") + str(uuid.uuid4())[:5]
    users[email] = {
        'name': name,
        'username': username,
        'password': password,
        'pin': pin,
        'balance': balance,
        'user_emoji': user_emoji
    }
    save_json(USERS_FILE, users)
    return username
    
def login_user(email, password):
    users = load_json(USERS_FILE)
    user = users.get(email)
    if user and user['password'] == password:
        loading_az()
        time.sleep(0.5)
        user_dashboard(user)
        return user
    else:
        print(Fore.RED + "\n🚨 Invalid credentials 🙊 ")
        time.sleep(2)
        return None
        
def user_dashboard(user):
    while True:
        load_json(GROUPS_FILE)
        load_json(FUSERS_FILE)
        load_json(GMESSAGES_FILE)
        load_json(MESSAGES_FILE)
        load_json(SHOP_FILE)
        load_json(TRANSACTIONS_FILE)
        user_data = load_json(USERS_FILE)
        clear_screen()
        print(Fore.BLUE + "="*40)
        print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "DE WORLD 🌏".center(40))
        print(Fore.BLUE + "="*41)
        print(Fore.GREEN + f"️${user['balance']}".center(40))
        print(Fore.BLUE+"_"*41)
        print(Fore.YELLOW+"\n What's on your mind?".center(40))
        print(Fore.BLUE+"_"*41)
        print(Fore.CYAN + "\n1. 🛍️ Shoping   |   2. ️🧑‍🔧 Menu")
        print(Fore.BLUE+"_"*40)
        print(Fore.CYAN+"\n3. 📩 Messages   |   4. 👥 Friends")
        print(Fore.BLUE+"_"*41)
        print(Fore.CYAN+"\n5. 🔍 Search   |   6. 📊 WSR-Fund")
        print(Fore.BLUE+"_"*41)
        print(Fore.CYAN+"\n7. 🫂 Groups   |   8. ⚙️ Settings")
        print(Fore.BLUE+"_"*41)
        print(Fore.CYAN+"\n0. 🛑 Logout ")
        print(Fore.BLUE+"_"*40)
        choice= input(Fore.CYAN+"\nPick What's on your mind: ")
        if choice == '1':
            Jet_shop(user)
        elif choice =='2':
            menu(user)
        elif choice == '3':
            my_friends(user, friends)
        elif choice == '4':
            my_friends(user, friends)
        elif choice == '5':
            search(user, group)
        elif choice == '6':
            wsr_fund(user)
        elif choice == '7':
            group(user)
        elif choice == '8':
            settings(user)
        elif choice == '0':
            print(Fore.RED+"Logging out...")
            time.sleep(4)
            return main_menu()
        else:
            print(Fore.RED+"No item found with the input")
            time.sleep(3)
            return user_dashboard(user)
            
def menu(user):
    clear_screen()
    print(Fore.BLUE + "=" * 40)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "MENU".center(40))
    print(Fore.BLUE + "=" * 40)

    print(Fore.GREEN + "1. Pay a User")
    print(Fore.GREEN + "2. Deposit Money")
    print(Fore.GREEN + "0. Exit")
    
    choice = input(Fore.BLUE + "\nSelect an option: ").strip()
    
    if choice == '1':
        pay(user)
    elif choice == '2':
        deposit(user)
    elif choice == '0':
        return user_dashboard(user)  # Return to the user dashboard
    else:
        print(Fore.RED + "Invalid option. Please try again.")
        time.sleep(1.5)
        return menu(user)

def pay(user):
    # Load users data from USERS_FILE
    users = load_json(USERS_FILE)
    
    # Prompt for recipient's username
    recipient_username = input(Fore.BLUE + "Enter the username of the person to pay: ").strip()
    
    # Check if the recipient exists
    if recipient_username not in users:
        print(Fore.RED + "User not found.")
        time.sleep(1.5)
        return menu(user)
    
    # Prompt for amount to pay
    try:
        amount = float(input(Fore.BLUE + "Enter the amount to pay: ").strip())
        if amount <= 0:
            raise ValueError("Amount must be greater than 0")
    except ValueError:
        print(Fore.RED + "Invalid amount.")
        time.sleep(1.5)
        return pay(user)
    
    # Check if the user has enough balance
    if users[user['email']]['balance'] < amount:
        print(Fore.RED + "Insufficient balance.")
        time.sleep(1.5)
        return menu(user)
    
    # Deduct the amount from the user's balance and add to the recipient's balance
    users[user['email']]['balance'] -= amount
    users[recipient_username]['balance'] += amount
    
    # Save the updated data to USERS_FILE
    save_json(USERS_FILE, users)
    
    print(Fore.GREEN + f"Payment of {amount} to {recipient_username} was successful.")
    time.sleep(1.5)
    return menu(user)

def deposit(user):
    # Load users data from USERS_FILE
    users = load_json(USERS_FILE)
    
    # Prompt for deposit amount
    try:
        deposit_amount = float(input(Fore.BLUE + "Enter the amount to deposit: ").strip())
        if deposit_amount <= 0:
            raise ValueError("Amount must be greater than 0")
    except ValueError:
        print(Fore.RED + "Invalid amount.")
        time.sleep(1.5)
        return deposit(user)
    
    # Add the deposit amount to the user's balance
    users[user['email']]['balance'] += deposit_amount
    
    # Save the updated data to USERS_FILE
    save_json(USERS_FILE, users)
    
    print(Fore.GREEN + f"Deposit of {deposit_amount} was successful.")
    time.sleep(1.5)
    return menu(user)
    
def group(user):
    clear_screen()
    print(Fore.CYAN + "=" * 40)
    print(Back.BLUE + Style.BRIGHT + Fore.CYAN + "Groups".center(40))
    print(Fore.CYAN + "=" * 40)
    print(Fore.BLUE + "\na. ➕ Create a group  |  6. 🫂 My Group")
    print(Fore.CYAN + "_" * 40)
    print(Fore.BLUE+"\n0. Back")
    print(Fore.CYAN+"_"*40)
    mo = input(Fore.BLUE + "\nInput an option: ")
    
    if mo == 'a':
        create_group(user)
    elif mo == '6':
        my_groups(user, groups)
    elif mo == '0':
        return user_dashboard(user)
        
def create_group(user):
    clear_screen()
    print(Fore.BLUE + "=" * 40)
    print(Back.BLUE + Style.BRIGHT + Fore.CYAN + "Create a Group".center(40))
    print(Fore.BLUE + "=" * 40)
    
    groups = load_json(GROUPS_FILE)
    
    while True:
        group_name = input(Fore.BLUE + "Enter the name of your group: ").strip()
        
        # Check if the group name is valid (non-empty)
        if not group_name:
            print(Fore.RED + "Group name cannot be empty.")
            continue
        
        # Check if the group already exists
        if group_name not in groups:
            # Add the new group to the groups file with the creator's username
            groups[group_name] = {
                'members': [user['username']]  # Assuming 'username' is the user's identifier
            }
            
            save_json(GROUPS_FILE, groups)
            print(Fore.GREEN + "Group created successfully.")
            time.sleep(0.8)
            return group(user)
        else:
            # Group already exists
            print(Fore.RED + f"Group already exists with this name: {group_name}")
            fg = input(Fore.BLUE + "Input 0 to create a new group, or 00 to return: ")
            
            if fg == '0':
                return create_group(user)  # Prompt the user again for a new group name
            elif fg == '00':
                return group(user)
            else:
                print(Fore.RED + "Invalid input. Please try again.")
            
def my_groups(user, groups):
    clear_screen()
    
    groups_data = load_json(GROUPS_FILE)
    user_groups = []  # List to store groups the user has joined or created
    
    # Iterate through all groups and check if the user is either a member or the creator
    for group_name, group_info in groups_data.items():
        if user['username'] in group_info.get('members', []):
            user_groups.append(group_name)

    print(Fore.BLUE + "=" * 40)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "YOUR GROUPS".center(40))
    print(Fore.BLUE + "=" * 40)
    
    if not user_groups:
        print(Fore.CYAN + "\nYou are not a member of any groups.")
        print(Fore.BLUE + "=" * 40)
        time.sleep(1.5)
        return user_dashboard(user)
    
    # Display the list of groups
    print(Fore.BLUE + "\n0. ↩️ Back")
    print(Fore.CYAN + "_" * 40)
    for idx, group in enumerate(user_groups, 1):
        print(Fore.GREEN + f"\n{idx}. {group}")
    
    print(Fore.CYAN + "_" * 40)
    
    # Prompt user to select a group
    cf = input("\nOpen a chat with a specific group (number): ")
    
    if cf == '0':  # Option to go back
        return user_dashboard(user)
    
    # Validate the user input and open the chat
    if cf.isdigit() and 1 <= int(cf) <= len(user_groups):
        selected_index = int(cf)
        selected_group = user_groups[selected_index - 1]
        print(f"\nOpening group chat for {selected_group}...")
        time.sleep(1.5)
        return group_chat(user, selected_group)  # Call the chat function with the selected group
    else:
        print("\nInvalid input. Returning to the group list...")
        time.sleep(1.5)
        return my_groups(user)

def clear_screen():
    """Clears the terminal screen."""
    print("\033c", end="")

def get_terminal_width():
    """Get the width of the terminal."""
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception as e:
        print(f"Error detecting terminal size: {e}")
        return 80  # Default width if detection fails

def format_message_box(user, message, width=30, align='left'):
    """Format a message into a box with the sender's username inside."""
    # Combine the username and message, with username at the top
    content = f"{user['username']}:\n{message}"
    
    # Wrap the content based on the provided width
    lines = textwrap.wrap(content, width=width)
    
    # Adjust alignment for each line (left or right)
    if align == 'right':
        lines = [line.rjust(width) for line in lines]
    elif align == 'left':
        lines = [line.ljust(width) for line in lines]

    # Create the message box with borders
    box = '\n'.join(f"║ {line} ║" for line in lines)
    top_bottom_border = '╔' + '═' * (width + 2) + '╗'
    
    return top_bottom_border + '\n' + box + '\n' + '╚' + '═' * (width + 2) + '╝'

def format_time_difference(timestamp):
    """Format time difference from timestamp to now."""
    try:
        message_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - message_time

        seconds = delta.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            return f"{int(days)}d"
        elif hours > 0:
            return f"{int(hours)}hr"
        elif minutes > 0:
            return f"{int(minutes)}m"
        else:
            return "0s"
    except ValueError:
        return "Invalid time"

def display_group_chat(messages, chat_key, selected_group, user):
    start_auto_refresh()
    """Display the chat history with sender usernames inside their messages."""
    clear_screen()
    print(Fore.BLUE + "=" * 40)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + f"{selected_group} Group Chat".center(40))
    print(Fore.CYAN + "=" * 40)
    
    terminal_width = get_terminal_width()
    message_width = terminal_width - 4  # Leave some padding for borders

    if chat_key in messages:
        print(Fore.BLUE + "\n"+"Chat History".center(40))
        print(Fore.BLUE+"="*40)
        for message in messages[chat_key]:
            sender_username = message['sender']  # Get the actual sender's username

            if sender_username == user['username']:
                # Right-aligned message box with username inside
                formatted_message = format_message_box(message['message'], width=message_width, align='right')
                print(Fore.GREEN + Style.DIM + f"{sender_username}".rjust(message_width) + Style.RESET_ALL)
                print(Fore.BLUE + Back.WHITE + formatted_message + Style.RESET_ALL)
            else:
                # Left-aligned message box with username inside
                formatted_message = format_message_box(message['message'], width=message_width, align='left')
                print(Fore.GREEN + Style.DIM + f"{sender_username}".ljust(message_width) + Style.RESET_ALL)
                print(Fore.WHITE + Back.BLUE + formatted_message + Style.RESET_ALL)
            
            # Display the time difference below the message
            time_diff = format_time_difference(message['timestamp'])
            print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo messages yet.")
    print(Fore.CYAN + "_" * 40)
    
def group_chat(user, selected_group):
    clear_screen()
    
    # Load messages from the file
    try:
        with open("gmessages.json", "r") as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        messages = {}  # Initialize if the file is empty or invalid

    # Generate a unique chat key based on the group name
    chat_key = f"group_{selected_group}"
    
    # Display chat history for the group
    display_group_chat(messages, chat_key, selected_group, user)

    while True:
        user_input = input(Fore.CYAN + "\nType a message, (or type 'exit' to leave the chat): ")
        if user_input.lower()== 'refresh':
            display_group_chat(messages, chat_key, selected_group, user)
        if user_input.lower() == 'exit':
            return my_groups(user, groups)
        
        if user_input.startswith('delete/'):
            command = user_input[7:]
            if command == 'all':
                # Delete all messages sent by the user
                deleted_count = delete_all_user_messages(messages, chat_key, user)
                print(Fore.RED + f"Deleted {deleted_count} messages sent by you.")
            else:
                # Delete messages containing the specified text
                deleted_count = delete_messages(messages, chat_key, command)
                print(Fore.RED + f"Deleted {deleted_count} messages containing '{command}'.")
            
            # Save the updated messages to gmessages.json
            with open("gmessages.json", "w") as file:
                json.dump(messages, file, indent=4)
            
            # Redisplay chat history
            display_group_chat(messages, chat_key, selected_group, user)
            continue
        
        new_message = {
            "sender": user['username'],
            "message": user_input,
            "timestamp": datetime.now().isoformat()  # Store timestamp in ISO format
        }
        
        if chat_key not in messages:
            messages[chat_key] = []
        
        messages[chat_key].append(new_message)
        
        # Save the updated messages to gmessages.json
        with open("gmessages.json", "w") as file:
            json.dump(messages, file, indent=4)
        
        display_group_chat(messages, chat_key, selected_group, user)
        
        print(Fore.RED + Style.DIM + "(just now)" + Style.RESET_ALL)  # Display "just now" in a smaller font style
        time.sleep(0.5)
     
    return my_groups(user)

def delete_all_user_messages(messages, chat_key, user):
    """Delete all messages sent by the current user in a chat."""
    if chat_key in messages:
        original_count = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if msg['sender'] != user['username']]
        deleted_count = original_count - len(messages[chat_key])
        return deleted_count
    return 0

def delete_messages(messages, chat_key, text):
    """Delete all messages that contain the specified text."""
    if chat_key in messages:
        original_count = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if text not in msg['message']]
        deleted_count = original_count - len(messages[chat_key])
        return deleted_count
    return 0
        
def new_message():
    with open("gmessages.json", "w") as file:
            json.dump(messages, file, indent=4)
  
load_json(GROUPS_FILE)
load_json(USERS_FILE)
load_json(FUSERS_FILE)        
def search(user, group):
    while True:
        load_json(GROUPS_FILE)
        load_json(USERS_FILE)
        load_json(FUSERS_FILE)
        clear_screen()  # Invoke the clear screen function
        print(Fore.CYAN + "=" * 40)
        print(Back.BLUE + Style.BRIGHT + Fore.CYAN + "🔍 SEARCH".center(40))
        print(Fore.CYAN + "=" * 40)
        print(Fore.BLUE+"Discover more".center(40))
        print(Fore.CYAN+"_"*40)
        print(Fore.BLUE+"\n1. 🫂 Groups   |   2. 👥 Friends")
        print(Fore.CYAN+"_"*40)
        print(Fore.BLUE + "\n0. Back")
        print(Fore.CYAN + "_" * 40)
    
        cb = input(Fore.BLUE + "\nwhat do you want to Discover? ")
        if cb == '0':
            return user_dashboard(user)
        elif cb == '1':
            find_groups(user, groups)
        elif cb == '2':
            find_friends(user, friends)
        else:
            print(Fore.RED+"invalid Input")
            return search(user, group)
  
GROUPS_FILE = 'groups.json'
groups = load_json(GROUPS_FILE)

def find_groups(user, groups):
    while True:
        GROUPS_FILE = 'groups.json'
        groups = load_json(GROUPS_FILE)
        load_json(GROUPS_FILE)
        clear_screen()
        print(Fore.BLUE + "=" * 40)
        print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "Discover Groups".center(40))
        print(Fore.BLUE + "=" * 40)
    
        fg = input(Fore.CYAN + "\nEnter the name of the group to discover or 0 to go back: ").strip()
    
        if fg == '0':
            return search(user, groups)  # Return to search or previous function
    
        group_found = False
    
        # Loop through groups to find a match
        for group_name in groups.keys():
            if fg.lower() == group_name.lower():  # Case-insensitive match
                group_found = True
                print(Fore.CYAN + f"Group found: {group_name}")
            
                # Prompt the user to join the group
                jg = input(Fore.BLUE + "\nDo you want to join this group? (Yes/No): ").strip().lower()
                if jg == 'yes':
                    save_group(user, group_name)
                    return  # Exit after joining
                elif jg == 'no':
                    print(Fore.RED + "Canceling...")
                    time.sleep(0.9)
                    return find_groups(user, groups)  # Allow the user to search again
                else:
                    print(Fore.RED + "Invalid input.")
                    time.sleep(0.9)
                    return find_groups(user, groups)  # Re-prompt after invalid input
    
        # If no group was found
        if not group_found:
            print(Fore.RED + f"No group found with the name '{fg}'.")
            time.sleep(1.5)
            return find_groups(user, groups)  # Return to search again
            
def save_group(user, group_name):
    while True:
        groups = load_json(GROUPS_FILE)
    
        # Check if the user is already a member of the group
        if user['username'] in groups[group_name]['members']:
            print(Fore.RED + "You are already a member of this group.")
            time.sleep(0.7)
            return
    
    # Add the user to the group members list
        groups[group_name]['members'].append(user['username'])
    
    # Save the updated groups to the file
        save_json(GROUPS_FILE, groups)
    
        print(Fore.GREEN + "Joined the group successfully.")
        time.sleep(0.7)
    
        return search(user, group_name)
   
USERS_FILE = 'users.json'
users = load_json(USERS_FILE)
friends = load_json(FUSERS_FILE)        
def find_friends(user, friends):
    while True:
        USERS_FILE = 'users.json'
        users = load_json(USERS_FILE)
        friends = load_json(FUSERS_FILE)
        clear_screen()
        print(Fore.CYAN+"="*40)
        print(Back.BLUE+Style.BRIGHT+Fore.CYAN+"Find a friend".center(40))
        print(Fore.CYAN+"="*40)
        ff= input(Fore.BLUE+"\nWhat is your friend username or 0 to go Back: ")
        if ff == '0':
            return search(user, group)
        elif ff == user['username']:
            print(Fore.CYAN+"Your are trying to search yourself 🫤")
            time.sleep(1.3)
            return search(user, group)
        user_found = False
        for user_data in users.values():
            if ff == user_data['username']:
                user_found = True
                print(f"{user_data['name']}")
                cm = input(Fore.BLUE+"Add Friend (Yes/No) ")
                if cm == 'Yes':
                    save_friend(user, ff)
                elif cm == 'No':
                    print("Cancelling.... ")
                    time.sleep(0.9)
                    return search(user, group)
                else:
                    print("invalid input")
                    return search(user, group)
        if not user_found:
            print(Fore.YELLOW+"\nNo user found 🚫")
            time.sleep(0.9)
            return search(user, group)
        
def save_friend(user, friend_username):
    while True:
        friends = load_json(FUSERS_FILE)
    
    # Check if they are already friends
        if user['username'] in friends and friend_username in friends[user['username']]:
            print("\nYou are both already friends")
            time.sleep(1.4)
            return search(user, group)
    
    # Add user to the friends list if they are not already in the file
        if user['username'] not in friends:
            friends[user['username']] = []
    
    # Add the friend's username to the user's friends list
        friends[user['username']].append(friend_username)
    
    # Add the user's username to the friend's list to ensure mutual friendship
        if friend_username not in friends:
            friends[friend_username] = []
    
        if user['username'] not in friends[friend_username]:
            friends[friend_username].append(user['username'])
        
    # Save the updated friends list to the file
        save_json(FUSERS_FILE, friends)
        print(Fore.GREEN+"\nFriend request sent")
        time.sleep(1.6)
    
        return search(user, group)        
        
def my_friends(user, friends):
    while True:
        clear_screen()
        friends_list = load_json(FUSERS_FILE).get(user['username'], [])  # Load the friends list for the user
    
        print(Fore.BLUE+"="*40)
        print(Back.CYAN+Style.BRIGHT+Fore.BLUE+"FRIENDS".center(40))
        print(Fore.BLUE+"="*40)
    
        if not friends_list:  # If the user has no friends
            print(Fore.CYAN+"\nYou have no friends.")
            print(Fore.BLUE+"="*40)
            time.sleep(1.5)
            return user_dashboard(user)
    
    # Display the list of friends
        print(Fore.BLUE+"\n0. ↩️ Back")
        print(Fore.CYAN+"_"*40)
        for idx, friend in enumerate(friends_list, 1):
            print(Fore.GREEN+f"\n{idx}. {friend}")
    
        print(Fore.CYAN+"_"*40)
    
    # Prompt user to select a friend
        cf = input("\nOpen a chat with a specific friend (number): ")
    
        if cf == '0':  # Option to go back
            return user_dashboard(user)
    
    # Validate the user input and open the chat
        if cf.isdigit() and 1 <= int(cf) <= len(friends_list):
            selected_index = int(cf)
            selected_friend = friends_list[selected_index - 1]
            print(f"\nOpening chat with {selected_friend}...")
            time.sleep(1.5)
            return chat(user, selected_friend)  # Call the chat function with the selected friend
        else:
            print("\nInvalid input. Returning to the friends list...")
            time.sleep(1.5)
            return my_friends(user, friends)
        
def settings(user):
    clear_screen()
    print(Fore.BLUE+"="*40)
    print(Back.CYAN+Style.BRIGHT+Fore.MAGENTA+"Account settings".center(40))
    print(Fore.BLUE+"="*40)
    print(Fore.GREEN+f"{user['name']}".center(40))
    print(Fore.BLUE+"_"*40)
    print(Fore.CYAN+"\n1. 👤 Change Name  |  2. 🔐 Change Pass")
    print(Fore.BLUE+"_"*40)
    print(Fore.CYAN+"\n3. Change Email   |   4. Help")
    print(Fore.BLUE+"_"*40)
    print(Fore.CYAN+"0. Back")
    print(Fore.BLUE+"_"*40)
    st=input(Fore.YELLOW+"\ninput an Option: ")
    if st == '0':
        return user_dashboard(user)
    elif st == '1':
        change_name(user)
    elif st == '2':
        change_password(user)
    elif st == '3':
        change_email(users, user_email )
    elif st == '4':
        clear_screen()
        print(Fore.GREEN+"="*40)
        print(Fore.BLUE+"Help Center")
        print(Fore.GREEN+"="*40)
        print(Fore.BLUE+"\nDelete_messages: example: delete/hello bro, will delete hello bro ")
        print(Fore.YELLOW+"deleted_all_message: example:- delete/all will delete all messages ")
        xc=input("input 0 to Return: ")
        if xc == '0':
            return settings(user)
            
def change_name(user):
    # Load the users data from USERS_FILE
    users = load_json(USERS_FILE)
    
    # Prompt the user for a new name
    old_name = input(Fore.CYAN + "Enter your old name (or 0 to exit): ")
    if not old_name:
        print(Fore.RED + "Old name cannot be empty")
        time.sleep(0.6)
        return change_name(user)
    
    if old_name == '0':
        return settings(user)
    
    elif old_name == user['name']:
        new_name = input(Fore.BLUE + "Enter your new name (or 0 to exit): ").strip()
    
        if not new_name:
            print(Fore.RED + "Name cannot be empty.")
            time.sleep(0.6)
            return change_name(user)
    
        # Update the user's name in the users data
        if new_name == user['name']:
            print(Fore.RED + "This is already your name")
            time.sleep(0.7)
            return settings(user)
        
        # Update the name in the user object and the users dictionary
        user['name'] = new_name
        users[user['email']]['name'] = new_name  # Update in users dict
    
        # Save the updated users data back to USERS_FILE
        save_json(USERS_FILE, users)
        
        print(Fore.GREEN + "Your name has been updated successfully.")
        time.sleep(0.8)
        return settings(user)
    
def change_password(user):
    # Load the users data from USERS_FILE
    users = load_json(USERS_FILE)
    
    # Prompt the user for their current password
    current_password = input(Fore.BLUE + "Enter your current password (or 0 to exit): ").strip()
    if current_password == '0':
        return settings(user)
    
    # Verify the current password
    if users[user['email']]['password'] != current_password:
        print(Fore.RED + "Incorrect current password.")
        time.sleep(0.7)
        return
    
    # Prompt the user for a new password
    new_password = input(Fore.BLUE + "Enter your new password: ").strip()
    
    if not new_password:
        print(Fore.RED + "Password cannot be empty.")
        return
    
    # Confirm the new password
    confirm_password = input(Fore.BLUE + "Confirm your new password: ").strip()
    
    if new_password != confirm_password:
        print(Fore.RED + "Passwords do not match.")
        time.sleep(0.7)
        return
    
    # Update the password in the users data
    if user['email'] in users:
        users[user['email']]['password'] = new_password
        user['password'] = new_password  # Update the password in the user object
    
        # Save the updated users data back to USERS_FILE
        save_json(USERS_FILE, users)
        
        print(Fore.GREEN + "Your password has been updated successfully.")
    else:
        print(Fore.RED + "User not found.")
    
    time.sleep(0.7)
    return user_dashboard(user)

def send_verification_code(email, code):
    # Replace with your SMTP server details
    smtp_server = "smtp.gmail.com"  # Example SMTP server
    smtp_port = 587
    from_email = "de.world.org@gmail.com"
    
    # Use environment variables for security
    password = os.getenv("Alex12345#")

    msg = EmailMessage()
    msg.set_content(f"Your verification code: {code}")
    msg["Subject"] = "Email Verification Code"
    msg["From"] = from_email
    msg["To"] = email

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as smtp:
            smtp.starttls()
            smtp.login(from_email, password)
            smtp.send_message(msg)
        print(f"Verification code sent to {email}.")
    except Exception as e:
        print(f"Failed to send verification code: {e}")

def save_json(filename, data):
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
user_email = load_json(USERS_FILE)
def change_email(users, user_email):
    # Input old email
    old_email = input("Enter your old email: ")

    # Check if old email matches user's email
    if old_email == user_email:
         # Generate random verification code
        verification_code = random.randint(100000, 999999)

        # Send verification code to old email
        send_verification_code(old_email, verification_code)

        # Input verification code
        input_code = input("Enter the verification code received in your email: ")

        # Check if input code matches verification code
        if int(input_code) != verification_code:
            print("Invalid verification code.")
            return
        else:
            # Input new email
            new_email = input("Enter your new email: ")

        # Update email in users dictionary
        users[new_email] = users.pop(old_email)

    # Save updated users data
        save_json("users.json", users)

        print("Email changed successfully.")
        time.sleep(0.9)
        return
        
def get_terminal_width():
    """Get the width of the terminal."""
    try:
        return shutil.get_terminal_size((80, 20)).columns
    except Exception as e:
        print(f"Error detecting terminal size: {e}")
        return 80  # Default width if detection fails

def format_message_box(message, width=30, align='left'):
    """Format a message into a box with specified width and alignment."""
    lines = textwrap.wrap(message, width=width)
    if align == 'right':
        lines = [line.rjust(width) for line in lines]
    elif align == 'left':
        lines = [line.ljust(width) for line in lines]

    box = '\n'.join(f"║ {line} ║" for line in lines)
    top_bottom_border = '╔' + '═' * (width + 2) + '╗'
    
    return top_bottom_border + '\n' + box + '\n' + '╚' + '═' * (width + 2) + '╝'

def format_time_difference(timestamp):
    """Format time difference from timestamp to now, showing only the largest relevant time unit."""
    try:
        message_time = datetime.fromisoformat(timestamp)
        now = datetime.now()
        delta = now - message_time

        seconds = delta.total_seconds()
        minutes = seconds // 60
        hours = minutes // 60
        days = hours // 24

        if days > 0:
            return f"{int(days)}d"
        elif hours > 0:
            return f"{int(hours)}hr"
        elif minutes > 0:
            return f"{int(minutes)}ms"
        else:
            return "0ms"

    except ValueError:
        return "Invalid time"

def display_chat_history(messages, chat_key, selected_friend, user):
    """Display the chat history with proper message alignment."""
    clear_screen()
    print(Fore.BLUE + "=" * 40)
    print(Back.CYAN + Style.BRIGHT + Fore.BLUE + f"Chats with {selected_friend}".center(40))
    print(Fore.CYAN + "=" * 40)
    
    terminal_width = get_terminal_width()
    message_width = terminal_width - 4  # Leave some padding for borders

    if chat_key in messages:
        print(Fore.BLUE + "\n"+"Chat History".center(40))
        for message in messages[chat_key]:
            if message['sender'] == user['username']:
                # Sender's message (right-aligned with blue background)
                formatted_message = format_message_box(message['message'], width=message_width, align='right')
                print(Fore.BLUE + Back.WHITE + formatted_message + Style.RESET_ALL)
            else:
                # Receiver's message (left-aligned with white background)
                formatted_message = format_message_box(message['message'], width=message_width, align='left')
                print(Fore.WHITE + Back.BLUE + formatted_message + Style.RESET_ALL)
            
            # Print timestamp in a smaller font style
            time_diff = format_time_difference(message['timestamp'])
            print(Fore.RED + Style.DIM + f"({time_diff})" + Style.RESET_ALL)
    else:
        print(Fore.RED + "\nNo messages yet.")
    
    print(Fore.CYAN + "_" * 40)
    time.sleep(0.9)

def delete_messages(messages, chat_key, text):
    """Delete messages containing the specified text."""
    if chat_key in messages:
        original_length = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if text not in msg['message']]
        return original_length - len(messages[chat_key])
    return 0

def delete_all_user_messages(messages, chat_key, user):
    """Delete all messages sent by the specified user."""
    if chat_key in messages:
        original_length = len(messages[chat_key])
        messages[chat_key] = [msg for msg in messages[chat_key] if msg['sender'] != user['username']]
        return original_length - len(messages[chat_key])
    return 0

def chat(user, selected_friend):
    clear_screen()
    
    # Try to load the messages from the file, handle if file is empty or missing
    try:
        with open("messages.json", "r") as file:
            messages = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):  # Catch missing or invalid file
        messages = {}  # Initialize an empty dictionary if file is empty or invalid

    # Generate a unique chat key using both usernames (sorted alphabetically)
    chat_key = f"{min(user['username'], selected_friend)}-{max(user['username'], selected_friend)}"
    
    # Display initial chat history
    display_chat_history(messages, chat_key, selected_friend, user)

    # Input loop to keep the chat active
    while True:
        user_input = input(Fore.CYAN + "\nType a message, (or type 'exit' to leave the chat): ")
        
        if user_input.lower() == 'exit':
            return my_friends(user, friends)
        
        if user_input.startswith('delete/'):
            command = user_input[7:]
            if command == 'all':
                # Delete all messages sent by the user
                deleted_count = delete_all_user_messages(messages, chat_key, user)
                print(Fore.RED + f"Deleted {deleted_count} messages sent by you.")
            else:
                # Delete messages containing the specified text
                deleted_count = delete_messages(messages, chat_key, command)
                print(Fore.RED + f"Deleted {deleted_count} messages containing '{command}'.")
            
            # Save the updated messages to messages.json
            with open("messages.json", "w") as file:
                json.dump(messages, file, indent=4)
            
            # Redisplay chat history
            display_chat_history(messages, chat_key, selected_friend, user)
            continue

        # Create a new message entry
        new_message = {
            "sender": user['username'],
            "message": user_input,
            "timestamp": datetime.now().isoformat()  # Store timestamp in ISO format
        }

        # Add the message to the conversation history
        if chat_key not in messages:
            messages[chat_key] = []
        
        messages[chat_key].append(new_message)
        
        # Save the updated messages to messages.json
        with open("messages.json", "w") as file:
            json.dump(messages, file, indent=4)

        # Immediately display the sent message in chat history
        display_chat_history(messages, chat_key, selected_friend, user)
        
        print(Fore.RED + Style.DIM + "(just now)" + Style.RESET_ALL)  # Display "just now" in a smaller font style
        time.sleep(0.5)  # Simulate message being sent

    return my_friends(user, friends)  # Return to the friends list after exiting the chat

def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')    
        
def wsr_fund(user):
    while True:
        clear_screen()
        print(Fore.CYAN + "="*40)
        print(Back.CYAN + Style.BRIGHT + Fore.BLUE + "WHISPER FUNDRAISER".center(40))
        print(Fore.CYAN + "="*40)
        print(Fore.BLUE + f"Welcome {user['name']}".center(40))
        print(Fore.CYAN + "_"*40)
        print(Fore.BLUE + "\n1. 🚆 Support WHISPER  |  2. 💲 Monetize")
        print(Fore.CYAN + "_"*40)
        print(Fore.BLUE + "\n0. Back")
        print(Fore.CYAN + "_"*40)

        choice = input("\nPick a choice or press enter 0 to go back....: ")
        
        if choice == '1':
            support(user)  # Ensure this function is defined elsewhere
            break
        elif choice == '2':
            monetize(user)  # Ensure this function is defined elsewhere
            break
        elif choice == '0' or choice == '':
            return user_dashboard(user)
        else:
            print(Fore.RED + "Invalid input, please try again.")
            time.sleep(2)
            
def support(user):
    clear_screen()
    btc="bc1qujwwt6gy9j5tfrapjgz6avfdh5xlt6huh4zk64"
    print(Fore.BLUE+"="*40)
    print(Back.CYAN+Style.BRIGHT+Fore.BLUE+"Support WHISPER".center(40))
    print(Fore.BLUE+"="*40)
    print(Fore.CYAN+"\n1. Support With BTC")
    print(Fore.BLUE+"_")
    print(Fore.CYAN+"0. Back")
    print(Fore.BLUE+"_"*40)
    choiice=input("\n pick an option: ")
    if choiice == '0':
        return wsr_fund(user)
    elif choiice == '1':
        print(Fore.GREEN+ f"Make a support to the address: {btc}")
        ret=input("input 0 to go back... ")
        if ret == '0':
            return wsr_fund(user)
        else:
            print(Fore.RED+"Invalid input")
            return wsr_fund(user)
    else:
        print(Fore.RED+"invalid input")
        time.sleep(1.5)
        return support(user) 
        
def monetize(user):
    clear_screen()
    print(Fore.CYAN + "=" * 40)
    print(Back.CYAN+ Style.BRIGHT+Fore.BLUE + f"Welcome to WHISPER Monetizing {user['name']}".center(40))
    print(Fore.CYAN + "=" * 40)
    print(Fore.RED + "\nComing soon...")
    fo = input(Fore.CYAN + "Enter 0 to return... ")
    if fo == '0':
        return wsr_fund(user)
    else:
        print(Fore.RED+"invalid input")
        return monetize(user)             
            
def main_menu():
    while True:
        # Start refreshing data automatically
        start_auto_refresh() 
        clear_screen()
        loading_az()
        clear_screen()
        print(Fore.CYAN + "="*40)
        print(Back.CYAN+ Style.BRIGHT+Fore.BLUE +"️DE WORLD 🌏".center(40))
        print(Fore.CYAN + "="*40)
        print(Fore.RED + "By proceeding, you agree to keep your information encrypted and stored under your service.".center(40))
        print(Fore.CYAN + "_"*40)
        print(Fore.BLUE + "\n1. Login   |   Exit [CTRL+Z]")
        print(Fore.CYAN+"_"*40)
        print(Fore.BLUE + "\n2. Create an account")
        print(Fore.CYAN+"_"*40)
        choice = input(Fore.CYAN + "\nPick a choice: ")
        
        if choice == '1':
            clear_screen()
            print(Fore.CYAN + "="*40)
            print(Back.CYAN+ Style.BRIGHT+Fore.BLUE + "DE WORLD 🌏".center(40))
            print(Fore.CYAN + "="*40)
            print(Fore.BLUE + "Login to your account".center(40))
            print(Fore.CYAN + "_"*40)
            email = input(Fore.CYAN + "\nEnter your email: ")
            password = input(Fore.GREEN + "\nEnter your password 🙈: ")
            login_user(email, password)
            
        elif choice == '2':
            clear_screen()
            print(Fore.CYAN + "="*40)
            print(Back.BLUE+ Style.BRIGHT+Fore.BLUE + "JOIN DE WORLD 🌏".center(40))
            print(Fore.CYAN + "="*40)
            print(Fore.GREEN+"\n Create an account and connect with friends and family privately.".center(40))
            print(Fore.CYAN + "_"*40)
            name = input(Fore.BLUE + "\nWhat is your full name: ")
            email = input(Fore.CYAN+"\nWhat is your email: ")
            password = input(Fore.BLUE + "\nCreate a password 🙈: ")
            pin= input(Fore.GREEN+"\nCreate a pin 🙈: ")
            username = register_user(name, email, password, pin)
            if username:
                print(Fore.GREEN + f"\nYour DE WORLD 🌏 account is created successfully! Username: {username}")
                input("\nPress Enter to return to the main menu...")
                
        elif choice == '0':
            loading_az()
            print(Fore.RED + "Exiting...")
            time.sleep(4)
            clear_screen()
            break
            
        else:
            print(Fore.RED + "\nInvalid input.")
            time.sleep(2)
            return main_menu()
            
if __name__ == "__main__":
    main_menu()                    
# Start refreshing data automatically
start_auto_refresh()             
            