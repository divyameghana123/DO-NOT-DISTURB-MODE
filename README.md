How This Project Works (Brief Explanation)
The Do Not Disturb (DND) Mode project temporarily blocks distracting websites by modifying the hosts file. It uses Python, Streamlit (for UI), and the subprocess module to automate the process.

🔹 Step-by-Step Working Process
1️⃣ User Opens the Streamlit App

The user enters the duration for which websites should be blocked (e.g., 30 minutes).

Clicks the "Activate DND Mode" button.

2️⃣ Blocking Websites

The program runs modify_hosts.py (a helper script) using subprocess.

This script adds entries to the hosts file, redirecting blocked websites to 127.0.0.1, making them inaccessible.

A message "Websites are blocked!" is displayed.

3️⃣ Waiting for the Set Time

The program pauses execution using time.sleep(duration).

The websites remain blocked during this period.

4️⃣ Unblocking Websites

Once the timer ends, modify_hosts.py runs again but now removes the blocked websites from the hosts file.

A message "Websites are unblocked!" is displayed.
