import streamlit as st
import os
import platform
import subprocess
from datetime import datetime, timedelta

hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
redirect = "127.0.0.1"

# Function to check DND status
def check_dnd_status():
    """Check if Focus Assist (Do Not Disturb) is enabled on Windows."""
    if platform.system() == "Windows":
        try:
            result = subprocess.run(
                ["powershell", "-Command", "(Get-ItemProperty -Path 'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings').FocusAssist"],
                capture_output=True, text=True
            )
            status = result.stdout.strip()
            return "🟢 ON" if status == "2" else "🔴 OFF"
        except Exception as e:
            return f"Error: {e}"
    return "Feature not available on this OS"

# Function to enable/disable DND
def toggle_dnd(mode):
    """Enable or disable Do Not Disturb (Focus Assist)"""
    if platform.system() == "Windows":
        value = "2" if mode == "true" else "0"  # 2 = ON, 0 = OFF
        os.system(f'powershell -Command "Set-ItemProperty -Path \'HKCU:\\Software\\Microsoft\\Windows\\CurrentVersion\\Notifications\\Settings\' -Name FocusAssist -Value {value}"')

# Function to block websites
def block_websites(websites):
    """Block specified websites by modifying the hosts file."""
    try:
        with open(hosts_path, "r+") as file:
            content = file.read()
            for website in websites:
                if website not in content:
                    file.write(f"\n{redirect} {website}")
        return "Websites Blocked Successfully!"
    except Exception as e:
        return f"Error: {e}"

# Function to unblock websites
def unblock_websites(websites):
    """Unblock specified websites by modifying the hosts file."""
    try:
        with open(hosts_path, "r") as file:
            lines = file.readlines()
        with open(hosts_path, "w") as file:
            for line in lines:
                if not any(website in line for website in websites):
                    file.write(line)
        return "Websites Unblocked Successfully!"
    except Exception as e:
        return f"Error: {e}"

# Function to schedule a task using Windows Task Scheduler
def schedule_task(task_name, time, command):
    """Schedule a task using Windows Task Scheduler"""
    try:
        os.system(f'schtasks /create /tn "{task_name}" /tr "{command}" /sc once /st {time} /rl highest /f')
        return f"Task '{task_name}' scheduled at {time}!"
    except Exception as e:
        return f"Error scheduling task: {e}"

# Streamlit UI
st.title("Windows Do Not Disturb (Focus Assist) & Website Blocker with Scheduling")

# Display real-time DND status
current_status = check_dnd_status()
st.write(f"### Current DND Status: **{current_status}**")

# User input for websites to block
st.subheader("🌐 Enter Websites to Block")
websites_input = st.text_area("Enter websites (comma-separated, e.g., facebook.com, youtube.com)", "")
websites = [site.strip() for site in websites_input.split(",") if site.strip()]

# Manual Enable/Disable DND
if st.button("Enable DND & Block Websites Now"):
    toggle_dnd("true")
    if websites:
        msg = block_websites(websites)
        st.success(f"🔕 Do Not Disturb Mode Enabled! \n{msg}")
    else:
        st.warning("⚠ Please enter at least one website to block.")
    st.rerun()

if st.button("Disable DND & Unblock Websites Now"):
    toggle_dnd("false")
    if websites:
        msg = unblock_websites(websites)
        st.success(f"✅ Do Not Disturb Mode Disabled! \n{msg}")
    else:
        st.warning("⚠ Please enter at least one website to unblock.")
    st.rerun()

st.divider()

# Scheduling Section
st.subheader("📅 Schedule DND & Website Blocking")

# Time input for scheduling
start_time = st.time_input("⏰ Select Start Time (DND ON)", value=datetime.now().time())
end_time = st.time_input("⏰ Select End Time (DND OFF)", value=(datetime.now() + timedelta(hours=1)).time())

if st.button("Schedule DND Mode"):
    if start_time >= end_time:
        st.error("❌ End time must be after the start time!")
    elif not websites:
        st.error("❌ Please enter at least one website to block!")
    else:
        # Convert times to Windows Task Scheduler format (HH:MM)
        start_time_str = start_time.strftime("%H:%M")
        end_time_str = end_time.strftime("%H:%M")

        # Schedule Start Task
        start_command = f'python -c "import os; os.system(\'powershell -Command \\"Set-ItemProperty -Path HKCU:\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Notifications\\\\Settings -Name FocusAssist -Value 2\\"\'); os.system(\'python -c \\"import dnd_blocker; dnd_blocker.block_websites({websites});\\" \')"'
        start_msg = schedule_task("DND_Start", start_time_str, start_command)

        # Schedule End Task
        end_command = f'python -c "import os; os.system(\'powershell -Command \\"Set-ItemProperty -Path HKCU:\\\\Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Notifications\\\\Settings -Name FocusAssist -Value 0\\"\'); os.system(\'python -c \\"import dnd_blocker; dnd_blocker.unblock_websites({websites});\\" \')"'
        end_msg = schedule_task("DND_End", end_time_str, end_command)

        st.success(f"✅ {start_msg}\n✅ {end_msg}")

st.info("Note: This works only on Windows 10 & 11. Make sure to run as Administrator.")
