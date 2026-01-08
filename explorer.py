from flask import Flask, request, session, redirect, render_template_string
from persistent_node import Blockchain, Transaction, Wallet
import os

app = Flask(__name__)
app.secret_key = os.urandom(24).hex()
chaka_coin = Blockchain()

HTML_HEAD = """
<style>
    :root { --sidebar-bg: #1a202c; --main-bg: #f7fafc; --accent: #4299e1; --reward: #ed8936; }
    body { font-family: 'Inter', sans-serif; background: var(--main-bg); margin: 0; display: flex; }
    .sidebar { width: 260px; background: var(--sidebar-bg); color: white; height: 100vh; position: fixed; padding: 30px; box-sizing: border-box; }
    .main { margin-left: 260px; flex: 1; padding: 50px; }
    .card { background: white; border-radius: 15px; padding: 25px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 25px; }
    .stat-card { background: white; padding: 25px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: center; }
    .hash { font-family: monospace; background: #edf2f7; padding: 4px; border-radius: 4px; font-size: 0.8em; word-break: break-all; color: #4a5568; }
    .btn { padding: 12px; border-radius: 8px; border: none; font-weight: bold; cursor: pointer; text-decoration: none; color: white; display: block; text-align: center; }
</style>
"""

@app.route('/dashboard')
def dashboard():
    if 'private_key' not in session: return redirect('/')
    current_wallet = Wallet(session['private_key'])
    
    # Leaderboard HTML
    leaders = chaka_coin.get_leaderboard()
    lb_html = "<table style='width:100%'>"
    for rank, (addr, amt) in enumerate(leaders, 1):
        lb_html += f"<tr><td>#{rank}</td><td class='hash'>{addr[:12]}...</td><td><b>{amt} ₵</b></td></tr>"
    lb_html += "</table>"

    content = f"""
    <h1>Network Status</h1>
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px;">
        <div class="stat-card"><h3>My Balance</h3><h2>{chaka_coin.get_balance(current_wallet.address)} CHAKA</h2></div>
        <div class="stat-card"><h3>Global Blocks</h3><h2>{len(chaka_coin.chain)}</h2></div>
        <div class="stat-card"><h3>Mempool</h3><h2>{len(chaka_coin.mempool)} Txs</h2></div>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
        <div class="card"><h3>🏆 Top Miners</h3>{lb_html}</div>
        <div class="card">
            <h3>Actions</h3>
            <a href="/mine" class="btn" style="background:var(--reward)">Mine New Block (+50)</a>
            <hr>
            <form action="/send" method="post">
                <input type="text" name="receiver" placeholder="Receiver Address" style="width:100%; padding:10px; margin-bottom:10px;">
                <input type="number" name="amount" placeholder="Amount" style="width:100%; padding:10px; margin-bottom:10px;">
                <button type="submit" class="btn" style="background:var(--accent); width:100%">Send Transaction</button>
            </form>
        </div>
    </div>
    """
    sidebar = "<div class='sidebar'><h2>ChakaScan</h2><hr><a href='/dashboard' style='color:white'>Home</a><br><a href='/logout' style='color:#ff7675'>Logout</a></div>"
    return f"{HTML_HEAD}{sidebar}<div class='main'>{content}</div>"

# (Include your existing login, logout, mine, and send routes here)

if __name__ == '__main__':
    from waitress import serve
    print("🚀 ChakaScan Production server running on port 8080...")
    serve(app, host='0.0.0.0', port=8080) # Use port 8080 for web deployment