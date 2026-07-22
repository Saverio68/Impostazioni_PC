# Updating Plan — Gestione Modelli Ollama Locale

File di riferimento per aggiornare le configurazioni quando si aggiungono o rimuovono modelli da `ollama`.

## Files da aggiornare

| File | Percorso | Descrizione |
|---|---|---|
| Server Config | `~/.pi/ollama-server-config.json` | Parametri server Ollama |
| Agent Models | `~/.pi/agent/models.json` | Lista modelli, contextWindow, temperature, num_ctx ecc. |
| Readme | `README.md` | Descrizione progetto e struttura |
| Readme HTML | `Readme.html` | Riepilogo configurazioni in formato web |

---

## 1. Aggiungere un nuovo modello a Ollama

### Step 1: Installa il modello
```bash
ollama pull <nome-modello>:<tag>
# Esempio: ollama pull mistral:7b
```

### Step 2: Verifica l'installazione
```bash
ollama ls
```
Prendi nota di:
- Nome completo (es. `mistral:7b`)
- Dimensione in GB
- Supporto immagine (se disponibile)

### Step 3: Decidi i parametri
| Parametro | Valore consigliato per coding |
|---|---|
| contextWindow | 32768 / 65536 / 131072 (dipende dal modello) |
| maxTokens | 32768 oppure pari a contextWindow |
| num_ctx | Pari a contextWindow |
| temperature | 0.2 se per coding, 0.5 se per vision/multimodale |
| reasoning | `true` solo se il modello supporta chain-of-thought esplicito |
| input | `["text"]` o `["text", "image"]` se ha visione |

> 🔑 **Nota hardware:** Su Mac M4 48GB, ogni modello in memoria consuma ~la sua dimensione GB + overhead (~1-2 GB). Con più runner attivi tieni sotto controllo il totale per evitare OOM.

### Step 4: Aggiungi il modello a models.json
All'interno del blocco `"ollama"` → `"models"`, aggiungi un nuovo oggetto prima degli altri o in posizione opportuna:

```json
{
  "contextWindow": <valore>,
  "maxTokens": <valore>,
  "id": "<nome-modello>:<tag>",
  "input": ["text"],
  "reasoning": true,
  "options": {
    "num_ctx": <stesso di contextWindow>,
    "temperature": <0.2 oppure 0.5>,
    "top_p": 0.9,
    "num_predict": <valore pari a maxTokens o più basso>,
    "input": ["text"]
  }
}
```

### Step 5: Commit e deploy
```bash
cd /Users/saverio/Development/pi_coding_agent/Impostazioni_PC
git add -A
git commit -m "feat: aggiungi modello <nome-modello> con parametri configurati"
git push origin master
git push ifac master
```

---

## 2. Rimuovere un modello da Ollama

### Step 1: Rimuovi il modello dal server
```bash
ollama rm <nome-modello>:<tag>
```

### Step 2: Rimuovi la configurazione da models.json
Elimina l'oggetto corrispondente dentro `"ollama"` → `"models"` in `~/.pi/agent/models.json`.

> ⚠️ **Attenzione:** se il modello rimosso era `_launch: true` (il default), spostalo sull'altro modello che userai di più.

### Step 3: Aggiorna Readme
Elimina la riga corrispondente nel file `Readme.html` all'interno della tabella dei modelli, e aggiorna anche `README.md`.

### Step 4: Commit e deploy
```bash
cd /Users/saverio/Development/pi_coding_agent/Impostazioni_PC
git add -A
git commit -m "chore: rimuovo modello <nome-modello> da configurazioni"
git push origin master
git push ifac master
```

---

## 3. Aggiornare i parametri di un modello esistente

Se vuoi modificare temperature, contextWindow, num_ctx o altri parametri:

1. Apri `~/.pi/agent/models.json`
2. Trova il blocco `"id": "<nome-modello>:<tag>"` (attenzione alle virgolette!)
3. Modifica i campi desiderati in place:
   ```json
   "options": {
     "num_ctx": 65536,
     "temperature": 0.1,
     "top_p": 0.95,
     "num_predict": 32768
   }
   ```
4. Aggiorna `Readme.html` e `README.md` con i nuovi valori
5. Commit e deploy come al solito

---

## 4. Checklist rapida di verifica

Dopo ogni modifica, esegui:

```bash
# 1. Verifica che il modello sia visibile sul server
ollama list | grep <nome-modello>

# 2. Controlla JSON valido (nessun errore di syntassi)
cat ~/.pi/agent/models.json | python3 -c "import json,sys; json.load(sys.stdin); print('✅ File valido')"

# 3. Verifica che i parametri siano coerenti
echo "Modello: <nome>"
echo "contextWindow === num_ctx? → Sì/Nu"
echo "maxTokens <= contextWindow? → Si/No"
echo "temperature logica (coding=0.2, vision=0.5)? → Si/No"

# 4. Push su entrambi i remotes
cd /Users/saverio/Development/pi_coding_agent/Impostazioni_PC
git add -A && git commit -m "config: <descrizione_modifica>" && git push origin master && git push ifac master
```

---

## 5. Notes & Warnings

- **Non versionare** mai i model files di Ollama (`.ollama/models/`, `.ollama/cache/`). Sono esclusi da `.gitignore`.
- **Non committare** mai segreti o API keys nei JSON. Se devi aggiungere variabili d'ambiente sensibili, usale come env vars esterne.
- **Sempre fare il backup prima di editare i JSON:** si può corrompere un file con virgole mancanti; meglio avere una copia sicura.
  ```bash
  cp ~/.pi/agent/models.json ~/.pi/agent/models.json.bak.$(date +%Y%m%d)
  ```
- Se hai più runner Ollama (es. per testing), tieni `max_runners_per_model=5` nel server config; su una sola macchina M4 con 48 GB, un runner alla volta è generalmente sufficiente e più sicuro per la stabilità.

---

*Ultimo aggiornamento Updating Plan: 23 Luglio 2026*
