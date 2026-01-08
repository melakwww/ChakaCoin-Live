from flask import Flask, request, session, redirect, render_template_string
from persistent_node import Blockchain, Transaction, Wallet
import os

app = Flask(__name__)
# Secure secret key for production
app.secret_key = os.urandom(24).hex() 
chaka_coin = Blockchain()

# RESPONSIVE UI: Ensures layout works on Desktop & Mobile
HTML_HEAD = """
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    :root { --sidebar-bg: #2c3e50; --main-bg: #f8fafc; --accent: #3498db; --reward: #e67e22; }
    body { font-family: 'Segoe UI', sans-serif; background: var(--main-bg); margin: 0; display: flex; }
    .sidebar { width: 250px; background: var(--sidebar-bg); color: white; height: 100vh; position: fixed; padding: 20px; box-sizing: border-box; }
    .main { margin-left: 250px; flex: 1; padding: 40px; }
    .card { background: white; border-radius: 12px; padding: 24px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); margin-bottom: 24px; }
    .stat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 30px; }
    .stat-card { background: white; padding: 20px; border-radius: 12px; border: 1px solid #e2e8f0; text-align: center; }
    .hash { font-family: monospace; background: #f1f5f9; padding: 4px 8px; border-radius: 4px; font-size: 0.85em; word-break: break-all; color: #475569; }
    .btn { padding: 12px 20px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; text-decoration: none; color: white; display: block; text-align: center; margin-top: 10px; }
    .btn-mine { background: var(--reward); width: 100%; }
    .btn-send { background: var(--accent); width: 100%; }
    
    @media (max-width: 768px) {
        body { flex-direction: column; }
        .sidebar { width: 100%; height: auto; position: relative; }
        .main { margin-left: 0; padding: 20px; }
        .stat-grid { grid-template-columns: 1fr; }
    }
</style>
"""

@app.route('/')
def index():
    if 'private_key' in session: return redirect('/dashboard')
    return f"""{HTML_HEAD}
    <div style="display:flex; align-items:center; justify-content:center; height:100vh; width:100%">
        <div class="card" style="width:350px; text-align:center">
            <h1>⛓️ ChakaScan</h1>
            <p>Access Node with Private Key</p>
            <form action="/login" method="post">
                <input type="password" name="private_key" placeholder="Private Key" style="width:100%; padding:10px; margin-bottom:15px; border-radius:4px; border:1px solid #ddd" required>
                <button type="submit" class="btn btn-send">Access Wallet</button>
            </form>
        </div>
    </div>"""

@app.route('/login', methods=['POST'])
def login():
    session['private_key'] = request.form['private_key']
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'private_key' not in session: return redirect('/')
    current_wallet = Wallet(session['private_key'])
    balance = chaka_coin.get_balance(current_wallet.address)
    
    # Leaderboard calculation for the UI
    leaders = chaka_coin.get_leaderboard()
    lb_html = "<h3>🏆 Top Miners</h3><table style='width:100%'>"
    for rank, (addr, amt) in enumerate(leaders, 1):
        lb_html += f"<tr><td>#{rank}</td><td class='hash'>{addr[:10]}...</td><td><b>{amt} ₵</b></td></tr>"
    lb_html += "</table>"
    
    content = f"""
    <h1>Wallet Overview</h1>
    <div class="stat-grid">
        <div class="stat-card"><h3>Balance</h3><p style="font-size: 2em; font-weight: bold;">{balance} CHAKA</p></div>
        <div class="stat-card"><h3>Mempool</h3><p style="font-size: 2em; font-weight: bold;">{len(chaka_coin.mempool)}</p></div>
        <div class="stat-card"><h3>Address</h3><p class="hash">{current_wallet.address[:12]}...</p></div>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 24px;">
        <div class="card">{lb_html}</div>
        <div class="card">
            <h3>Quick Actions</h3>
            <a href="/mine" class="btn btn-mine">🚀 Mine Block (+50 CHAKA)</a>
        </div>
    </div>
    """
    sidebar = f"<div class='sidebar'><h2>⛓️ ChakaScan</h2><hr><a href='/dashboard' style='color:white; text-decoration:none;'>Dashboard</a><br><br><a href='/logout' style='color:#ff7675; text-decoration:none;'>Logout</a></div>"
    return f"{HTML_HEAD}{sidebar}<div class='main'>{content}</div>"

@app.route('/mine')
def mine():
    if 'private_key' not in session: return redirect('/')
    current_wallet = Wallet(session['private_key'])
    chaka_coin.mine_pending_transactions(miner_address=current_wallet.address) 
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
