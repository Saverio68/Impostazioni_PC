# Updating Plan — Gestione Modelli Ollama Locale

File di riferimento per aggiornare le configurazioni quando si aggiungono o rimuovono modelli da `ollama`, ottimizzando l'ambiente Mac M4 48GB.

## 🚀 Approccio consigliato (Automazione)

Per la stragrande maggioranza delle modifiche, **non serve operare manualmente nei JSON**. Usa lo script incluso nella repository:

1. Esegui le tue operazioni di modello Ollama sul terminale:
   ```bash
   ollama pull <nome-modello>    # per aggiungere
   ollama rm   <nome-modello>    # per rimuovere
   ```
2. Rigenera automaticamente tutte le configurazioni locali (JSON server + JSON agent) e il riepilogo HTML con un solo comando da questa cartella:
   ```bash
   python3 scripts/config-update.py
   ```

Lo script legge `ollama list`, calcola i valori ottimali in base alla RAM del Mac M4 e alla categoria del modello, e aggiorna:
- `~/.pi/agent/models.json` (mappa dei modelli)
- `Readme.html` (aggiornamento visivo tabella)

3. Esegui il commit:
   ```bash
   git add -A && git commit -m "config: synced config with ollama models" && git push origin master && git push ifac master
   ```

---

## 📂 Files da gestire (in caso di manutenzione manuale)

Se preferisci o devi intervenire manualmente, ecco la struttura:

1. **`~/.pi/agent/models.json`** — Il cuore delle configurazioni. Contiene i parametri `contextWindow`, `maxTokens`, `num_ctx`, `temperature`, `reasoning` per ogni modello.
2. **`~/.pi/ollama-server-config.json`** — Parametri del server Ollama (inferenza, memoria GPU, etc.). Modificare solo se cambiano le regole di sistema di Ollama.
3. **`Readme.html`** e **`README.md`** — Documentazione locale. Lo script le aggiorna in automatico; in manuale vanno sincronizzate con i valori del JSON.

---

## 📝 Procedura di manutenzione (Manuale)

### Step 1: Verifica i modelli
```bash
ollama ls
```
Prendi nota di: `NAME`, `SIZE` e supporta immagini.

### Step 2: Regole per il mapping dei parametri
| Parametro | Logica di assegnazione |
|---|---|
| **contextWindow** | 131072 dove il modello lo supporta (es. Qwen3). Minore se limitato dal contesto nativo del modello. |
| **num_ctx** | Mai inferiore a 32768 su Mac M4 48GB per evitare swap. Se `contextWindow` > 65k, useremo un `num_ctx` di sicurezza pari a 65536 per stabilità VRAM. |
| **maxTokens / num_predict** | Sempre allineati al massimo output possibile (pari a `num_ctx` o superiore se richiesto dal modello). Valore alto (es. 65k) evita che il modello "zitti" a metà su sessione di coding lunghe. |
| **temperature** | 0.2 per Coding/Pure Text (preciso e ripetibile). 0.5 per Vision/Image (più adattivo). |
| **reasoning** | `true` solo per DeepSeek-R1, Ornith, Qwen3-Coder/Advanced. `false` per modelli standard o vision only. |

### Step 3: Modifica locale del JSON di configurazione
1. Apri `~/.pi/agent/models.json` come root user/sudo se hai permessi, oppure usa il tuo account (esiste in home directory): `~/.pi/agent/models.json`.
2. Cerca il blocco `"models": [` sotto provider `"ollama"`. Aggiungi o rimuovi gli oggetti JSON corrispondenti ai nuovi modelli di `ollama ls`.

### Step 4: Commit manuale (se non hai usato lo script)
Se hai operato manualmente, aggiorna anche `Readme.html` e `README.md` con i nuovi valori inseriti nella tabella dei parametri.

---

## ⚠️ Checklist e Avvertenze

- **Mac M4 48GB:** Puoi permetterti `num_ctx` elevati (fino a 65k/131k) senza crashare il sistema, ma evita di tenere *più runner Ollama attivi contemporaneamente* per lo stesso modello grande (es. Ornith o Qwen3 da 23GB), potresti saturare la RAM unificata (OOM).
- **Sicurezza:** I JSON contenenti `apiKey` sono solo placeholders; non committare mai chiavi API reali in repository pubblici su cui non hai controllo di accesso rigoroso.

---

*Piano di updating automatizzato per Mac M4/48GB. s.priori@ifac.cnr.it — Luglio 2026*
