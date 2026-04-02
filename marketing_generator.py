import os
from db_manager import DBManager

def generate_social_media_posts(db_path="data/cyber_shield.db"):
    db = DBManager(db_path=os.environ.get("DATABASE_URL", db_path))
    
    # Próba pobrania statystyk
    stats = db.get_stats()
    port_stats = db.get_custom_port_stats()
    
    total = stats.get('total_anomalies', 0)
    blocks = stats.get('active_blocks', 0)
    
    top_port = "SSH (22)"
    top_port_hits = 0
    if port_stats and 'labels' in port_stats and port_stats['labels']:
        top_port = port_stats['labels'][0]
        top_port_hits = port_stats['values'][0]

    # Szablony
    reddit_post = f"""
[Title] I built a 24/7 Honeypot that auto-blocks hackers. We just hit {total} attacks!

Hey r/SaaS and r/cybersecurity,

A while ago I deployed Cyber Shield AI - a custom honeypot network that logs malicious IP activities and serves them via an API.
Today I'm happy to announce that we've crossed **{total} attacks** logged and actively blocked **{blocks}** threats today.

Top targeted port over our network is currently **{top_port}** with **{top_port_hits}** unauthorized access attempts.

We just launched a live real-time dashboard to visualize this data in Chart.js directly at our API root:
🔗 https://threat-intelligence-api.onrender.com/

You can also use the API for your own applications (it's on RapidAPI, Free tier available).
Would love to hear your feedback on the dashboard and the data!
"""

    twitter_post = f"""
🛡️ Cyberattackers never sleep! 
Our Cyber Shield Honeypot just crossed {total} malicious activities detected and neutralized {blocks} active threats.

Top attack vector today: {top_port} ({top_port_hits} attempts). 

We just launched a live Dashboard to visualize this threat intel in real-time.
Check it out here: https://threat-intelligence-api.onrender.com/ 
#CyberSecurity #API #ThreatIntel #BuildInPublic
"""

    return {
        "reddit": reddit_post.strip(),
        "twitter": twitter_post.strip()
    }

if __name__ == "__main__":
    print("Generating Social Media Content based on Live DB Stats...\n")
    posts = generate_social_media_posts()
    
    print("=== REDDIT POST ===")
    print(posts["reddit"])
    print("\n" + "="*50 + "\n")
    print("=== TWITTER / X POST ===")
    print(posts["twitter"])
    print("\n" + "="*50 + "\n")
