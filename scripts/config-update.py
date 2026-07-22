#!/usr/bin/env python3
"""
auto_config.py: Aggiorna automaticamente le configurazioni Ollama e Agent
basandosi sui modelli attuali installati nel server locale.

Richiede 'ollama' CLI e Python 3.7+.
Esegui da /Users/saverio/Development/pi_coding_agent/Impostazioni_PC o specifica il path base della repo manualmente.
"""

import json
import subprocess
import sys
import os
from datetime import datetime

# ================= CONFIGURAZIONE HARDWARE E REGOLE =================

# Hardware specific del Mac M4 48GB (basato sui requisiti)
TOTAL_RAM_GB = 48

# Regole per il mapping dei modelli
MODEL_RULES = {
    "qwen3.6:latest": { "contextWindow": 131072, "reasoning": True, "input": ["text"] },
    "qwen3.6:35b": { "contextWindow": 131072, "reasoning": True, "input": ["text"] }, # Alias o variante
    "qwen3-coder:latest": { "contextWindow": 131072, "reasoning": True, "input": ["text"] },
    "qwen3-coder:30b": { "contextWindow": 32768, "reasoning": True, "input": ["text"] },
    "deepseek-r1:32b": { "contextWindow": 131072, "reasoning": True, "input": ["text"] },
    "ornith:35b-q4_K_M": { "contextWindow": 131072, "reasoning": True, "input": ["text"] },
    "llama3.2-vision:latest": { "contextWindow": 32768, "reasoning": False, "input": ["text", "image"] },
    "qwen3-vl:latest": { "contextWindow": 131072, "reasoning": False, "input": ["text", "image"] },
    "glm-ocr:latest": { "contextWindow": 32768, "reasoning": False, "input": ["text", "image"] },
}

# Valori default per modelli sconosciuti (fallback)
DEFAULT_CONTEXT = 8192
DEFAULT_REASONING = False
DEFAULT_INPUT = ["text"]


def get_ram_gb():
    """Legge la memoria totale di RAM dal sistema."""
    try:
        output = subprocess.check_output(["sysctl", "hw.memsize"]).decode("utf-8").strip()
        # Formato: hw.memsize: 51607630848
        ram_bytes = int(output.split(": ")[1])
        return ram_bytes / (1024**3)
    except Exception:
        print("⚠️ Impossibile rilevare RAM di sistema, uso valore fallback 48GB.")
        return TOTAL_RAM_GB


def get_ollama_models():
    """Esegue 'ollama list' e restituisce una lista di dizionari."""
    try:
        output = subprocess.check_output(["ollama", "list"]).decode("utf-8")
        models = []
        # Formato output: NAME               ID             SIZE      MODIFIED
        lines = output.strip().split('\n')
        if len(lines) < 2:
            print("Nessun modello trovato.")
            return models

        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 3:
                name = parts[0]
                size_str = parts[2] # es. "19 GB", "2.2 GB"
                
                # Parsing della dimensione per stimare se il modello sta in VRAM
                try:
                    val = float(size_str.split()[0])
                    unit = size_str.split()[1].upper()
                    if unit == 'GB':
                        size_bytes = val * 1e9
                    elif unit == 'MB':
                        size_bytes = val * 1e6
                    else:
                        size_bytes = val # assume bytes or unknown
                except:
                    size_bytes = 0

                models.append({ "name": name, "size_bytes": size_bytes })
        return models
    except Exception as e:
        print(f"Errore nell'esecuzione di 'ollama list': {e}")
        sys.exit(1)


def generate_config(models_list):
    """Genera il JSON configuration per agent."""
    providers = {
        "claude-code": {
            "api": "openai-completions",
            "apiKey": "claude-code",
            "baseUrl": "http://127.0.0.1:49413/v1",
            "models": [] # Mantiene le config Claude (non tocchiamo il cloud per ora)
        },
        "ollama": {
            "api": "openai-completions",
            "apiKey": "ollama",
            "baseUrl": "http://127.0.0.1:11434/v1",
            "models": []
        }
    }

    local_idx = 0
    
    for m in models_list:
        rule = MODEL_RULES.get(m["name"], None)
        
        if rule:
            # Regole personalizzate (da settings.md / hardware spec)
            ctx = rule["contextWindow"]
            reasoning = rule["reasoning"]
            inp = rule["input"]
            
            # Logica per maxTokens e num_predict basata su ContextWindow
            # num_predict deve sempre essere <= maxTokens ed equilibrato con hardware
            if ctx >= 131072:
                max_tok = 65536 
                num_ctx_cfg = 65536 # Safety cap per VRAM stability unless specific model needs more
            elif ctx >= 32768:
                max_tok = 32768
                num_ctx_cfg = ctx
            else:
                max_tok = 4096
                num_ctx_cfg = ctx
        else:
            # Fallback generico
            ctx = DEFAULT_CONTEXT
            reasoning = DEFAULT_REASONING
            inp = DEFAULT_INPUT
            max_tok = 8192
            num_ctx_cfg = 8192

        is_default = (local_idx == 0)

        models_list_json = [{
            "_launch": is_default,
            "contextWindow": ctx,
            "maxTokens": max_tok,
            "id": m["name"],
            "input": inp,
            "reasoning": reasoning,
            "options": {
                "num_ctx": num_ctx_cfg,
                "temperature": 0.2 if "vision" not in m["name"] else 0.5, # Default coding vs vision
                "top_p": 0.9,
                "num_predict": max_tok, # num_predict allineato a maxTokens come discusso
                "input": inp
            }
        }]

        providers["ollama"]["models"].extend(models_list_json)
        local_idx += 1
        
    return {
        "_global_defaults": {
            "contextWindow": 131072, 
            "maxTokens": 65536,
            "input": ["text"],
            "reasoning": False,
            "options": {"temperature": 0.2, "top_p": 0.9, "num_predict": 65536, "num_ctx": 131072}
        },
        "_mac_m4_48gb_notes": "Configurazioni generate automaticamente con auto_config.py. Num_predict allineato a maxTokens.",
        "providers": providers
    }


def generate_readme_html(config_data):
    """Genera l'HTML riepilogativo (Readme.html)."""
    
    html_models_rows = []
    ollama_models = config_data["providers"]["ollama"]["models"]

    for m in ollama_models:
        launch_tag = 'style="background-color: #3fb95022;"' if m["_launch"] else ''
        reasoning_badge = '<span class="badge ok">YES</span>' if m["reasoning"] else '<span class="badge info">NO</span>'
        
        row = f"""
      <tr {launch_tag}>
        <td><b>{m['id']}</b> {'<em>(Default)</em>' if m['_launch'] else ''}</td>
        <td>Dynamic</td>
        <td>{m['contextWindow']}</td>
        <td>{m['maxTokens']}</td>
        <td>{m['options']['num_ctx']}</td>
        <td>{m['options']['temperature']}</td>
        <td>{reasoning_badge}</td>
      </tr>"""
        html_models_rows.append(row)

    html = f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="UTF-8">
<title>Riepilogo Configurazioni - Impostazioni_PC (Generated)</title>
<style>
  body {{ font-family: sans-serif; background: #0d1117; color: #c9d1d9; padding: 20px; max-width: 900px; margin: auto; }}
  table {{ border-collapse: collapse; width: 100%; color: white; }}
  th, td {{ border: 1px solid #30363d; padding: 8px 12px; text-align: left; vertical-align: top; }}
  th {{ background-color: #161b22; color: #58a6ff; white-space: nowrap; }}
  tr:nth-child(even) td {{ background-color: #0d111744; }}
  .badge {{ display: inline-block; padding: 2px 8px; border-radius: 12px; font-size: 0.8em; vertical-align: middle; }}
  .ok {{ background: #238636; color: white; }}
  .info {{ background: #1f6feb; color: white; }}
  h2 {{ color: #58a6ff; }}
</style>
</head>
<body>

<span class="badge ok">Generated Auto by auto_config.py</span> {datetime.now().strftime('%d/%m/%Y')}

<h1>Riepilogo Configurazioni - Mac M4 48GB</h1>

<h2>Modelli Ollama Attivi</h2>
<table>
  <thead>
    <tr>
      <th>Modello</th>
      <th>Dimensione Stimata</th>
      <th>contextWindow</th>
      <th>maxTokens</th>
      <th>num_ctx</th>
      <th>temp.</th>
      <th>reasoning</th>
    </tr>
  </thead>
  <tbody>
    """ + "".join(html_models_rows) + f"""
  </tbody>
</table>

<h2>Note sui Parametri (num_predict)</h2>
<ul>
<li><b>num_predict:</b> Impostato sempre pari a <code>maxTokens</code> per evitare troncamenti precoci su sessioni lunghe.</li>
<li><b>temperature:</b> 0.2 per coding/reasoning (deterministico), 0.5 per visione (flessivo).</li>
<li><b>num_ctx:</b> Bilanciato tra capacità del modello e stabilità VRAM su Mac M4.</li>
</ul>

<p style="color: #8b949e;">Configuraioni generate automaticamente per Impostazioni_PC — s.priori@ifac.cnr.it</p>

</body>
</html>"""

    return html


def main():
    print("🔍 Rilevamento modelli Ollama...")
    models_list = get_ollama_models()
    
    if not models_list:
        print("⚠️ Nessun modello trovato. Esegui 'ollama ls' per verificare.")
        return

    print(f"✅ Trovati {len(models_list)} modelli. Generazione configurazione...")
    
    # 1. Genera config JSON
    config_data = generate_config(models_list)
    
    config_path = os.path.expanduser("~/.pi/agent/models.json")
    dir_path = os.path.dirname(config_path)
    if not os.path.isdir(dir_path):
        try: os.makedirs(dir_path)
        except OSError: pass

    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config_data, f, indent=2, ensure_ascii=False)
    print(f"✅ Configurazione salvata in: {config_path}")

    # 2. Genera Readme HTML (nella dir corrente o default)
    target_html = os.path.join(os.getcwd(), "Readme.html")
    html_content = generate_readme_html(config_data)
    with open(target_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"✅ Readme HTML salvato in: {target_html}")

if __name__ == "__main__":
    main()
