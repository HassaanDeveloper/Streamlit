import streamlit as st
import re
import random

st.set_page_config(page_title="Password Strength Meter", page_icon="🔐", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        .password-strength-weak { color: #ff0000; font-weight: bold; }
        .password-strength-moderate { color: #ff9900; font-weight: bold; }
        .password-strength-strong { color: #00cc00; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

st.title("🔐 Password Strength Meter")
st.markdown("### 🔍 Check your password security")

# Word lists for password generation
adjectives = ["Happy", "Smart", "Brave", "Swift", "Cool", "Wild", "Bright", "Calm", "Deep", "Fresh"]
nouns = ["Dragon", "Lion", "Eagle", "Tiger", "Bear", "Wolf", "Hawk", "Deer", "Fox", "Bird"]
numbers = ["123", "456", "789", "2088", "2025", "100", "500", "890", "777", "586"]
special_chars = ["@", "#", "$", "&", "*", "!", "?", "%", "+", "="]

def generate_memorable_password():
    # It will select random words and format them
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    num = random.choice(numbers)
    char = random.choice(special_chars)
    
    # different patterns like this:
    patterns = [
        f"{adj}{noun}{num}{char}",  # HappyDragon123@
        f"{adj}{char}{noun}{num}",  # Happy@Dragon123
        f"{noun}{adj}{num}{char}",  # DragonHappy123@
        f"{noun}{char}{adj}{num}",  # Dragon@Happy123
        f"{adj}{num}{noun}{char}",  # Happy123Dragon@
        f"{noun}{num}{adj}{char}"   # Dragon123Happy@
    ]
    
    return random.choice(patterns)

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    return score, feedback

# Password input
password = st.text_input("Enter your password:", type="password")

if password:
    score, feedback = check_password_strength(password)
    
    # Display strength rating
    st.markdown("### Password Strength Rating:")
    if score == 4:
        st.markdown('<p class="password-strength-strong">✅ Strong Password!</p>', unsafe_allow_html=True)
    elif score == 3:
        st.markdown('<p class="password-strength-moderate">⚠️ Moderate Password</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="password-strength-weak">❌ Weak Password</p>', unsafe_allow_html=True)
    
    # Display progress bar
    st.progress(score / 4)
    
    # Display feedback
    if feedback:
        st.markdown("### 💡 Suggestions for Improvement:")
        for message in feedback:
            st.info(message)
    
    # Display password criteria status
    st.markdown("### Password Criteria Status:")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("Length (≥8):")
        if len(password) >= 8:
            st.success(f"✅ {len(password)} characters")
        else:
            st.error(f"❌ {len(password)} characters")
            
        st.markdown("Uppercase & Lowercase:")
        if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
            st.success("✅ Contains both")
        else:
            st.error("❌ Missing one or both")
    
    with col2:
        st.markdown("Numbers:")
        if re.search(r"\d", password):
            st.success("✅ Contains numbers")
        else:
            st.error("❌ No numbers")
            
        st.markdown("Special Characters:")
        if re.search(r"[!@#$%^&*]", password):
            st.success("✅ Contains special chars")
        else:
            st.error("❌ No special chars")

# Password Generator:
st.markdown("### 🎲 Generate a Memorable Password")
col1, col2 = st.columns(2)

with col1:
    if st.button("🔄 Generate Memorable Password"):
        generated_password = generate_memorable_password()
        st.success(f"🔐 Generated Password: `{generated_password}`")
        st.info("✨ This password is secure and memorable as well!")

with col2:
    if st.button("🎲 Generate Random Password"):
        import string
        length = 12
        characters = string.ascii_letters + string.digits + "!@#$%^&*"
        random_password = ''.join(random.choice(characters) for _ in range(length))
        st.success(f"🔐 Generated Password: `{random_password}`")
        st.info("✨ This is a completely random secure password!")

# Password Generation Tips:
with st.expander("💡 Password Generation Tips"):
    st.markdown("""
    ### Memorable Password Tips:
    - Combine words with numbers and special characters
    - Use meaningful words that are easy to remember
    - Add your own twist to the generated passwords
    - Avoid using personal information
    - Make sure it's at least 8 characters long
    
    ### Example Patterns:
    - Word + Number + Special: `HappyDragon123@`
    - Word + Special + Number: `Dragon@2024`
    - Number + Word + Special: `2024Dragon@`
    
    ### Security Tips:
    - Don't use the same password for multiple accounts
    - Change passwords regularly
    - Never share your passwords
    - Use a password manager for better security
    """)

# Security Tips:
with st.expander("📝 Password Security Tips"):
    st.markdown("""
    - Use a unique password for each account
    - Avoid using personal information
    - Consider using a password manager
    - Change passwords regularly
    - Never share your passwords
    """)

