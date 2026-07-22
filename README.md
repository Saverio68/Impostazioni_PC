# Impostazioni_PC

Configurazioni locali di **Ollama** e del **pi coding agent** per un ambiente Mac M4 (Apple Silicon) con 48 GB RAM.

---

## 📌 Scope del progetto

Questo repository contiene solo i file di configurazione necessari per sincronizzare l'ambiente di lavoro con il server Ollama locale. Non include né genera codice — è puramente infrastrutturale:

- **Server Ollama config** → ottimizza inferenza per Mac M4 48GB
- **Agent models config** (pi coding agent) → mappa tutti i modelli disponibili con i loro parametri
- **Documentazione HTML** → riepilogo visivo delle configurazioni applicate
- **.gitignore** → protegge dati sensibili e pesanti

---

## 🗂️ Struttura dei files

```
Impostazioni_PC/
├── settings.md            # Istruzioni originali (non modificare)
├── Readme.html            # Riepilogo visivo configurazioni
├── README.md              # Questo file
├── updating_plan.md       # Guida aggiornare modili Ollama e sync config
└── .gitignore             # Esclude modelli, dati sensibili, etc.
```

### Files non-versionati (su disco locale)

| File | Percorso locale | Descrizione |
|---|---|---|
| Server Config | `~/.pi/ollama-server-config.json` | Parametri server Ollama |
| Agent Models | `~/.pi/agent/models.json` | Lista + parametri ogni modello |

---

## 🧭 Come usare l'Updating Plan

Quando cambi modelli sul server Ollama (aggiungi, rimuovi o modifica i parametri), usa [`updating_plan.md`](updating_plan.md) come procedura guidata.

### Riepilogo rapido:

1. **Aggiungere un modello** → `ollama pull <model>` → aggiungi a models.json → commit
2. **Rimuovere un modello** → `ollama rm <model>` → rimuovi da models.json + README → commit
3. **Modificare parametri** → edita il blocco nel JSON dell modello → aggiorna Readme.html → commit
4. Ogni volta che modifichi: esegui la [checklist rapida](updating_plan.md#5-checklist-rapida-di-verifica) prima del commit

### Backup automatico consigliato

Prima di qualsiasi modifica ai JSON, fai un backup:

```bash
cp ~/.pi/agent/models.json ~/.pi/agent/models.json.bak.$(date +%Y%m%d)
```

---

## 🔑 Parametri Chiave (spiegati)

| Parametro | Descrizione | Valore default usato |
|---|---|---|
| `contextWindow` | Finestrali contesto massima in token | 131072 dove possibile |
| `maxTokens` | Token massimi che il modello puo generare per risposta | Pari a contextWindow o limite inferiore |
| `num_ctx` | Numero di token effettivi nel sliding window attiva. Deve essere ≤ contextWindow | 65536 / 131072 |
| `temperature` | Creativity del modello: 0 = determinista, 1 = casuale | **0.2** per coding, **0.5** per vision |
| `top_p` | Nucleo sampling; filtra tokens con probabilità cumulativa < p | 0.9 (standard) |

---

## 🌐 Repository Remoti

L'ambiente sincronizzato su due piattaforme:

| Remote | URL | Scopo |
|---|---|---|
| **origin** (GitHub) | `github.com/Saverio68/Impostazioni_PC` | Backup e accessibilita internazionale |
| **ifac** (IFAC CNR) | `git.ifac.cnr.it/priori/impostazioni_pc` | Ambiente institutional / dipartimentale |

Comandi push:
```bash
git push origin master    # push su GitHub
git push ifac master      # push su IFAC CNR GitLab
```

---

## ⚙️ Hardware di riferimento

| Componente | Specifica |
|---|---|
| CPU / GPU | Apple M4 (Metal) |
| RAM | 48 GB unificata |
| OS | macOS Sonoma / Sequoia |
| Server Ollama | `/Users/saverio/.ollama/` |
| Agent Pi | `~/.pi/` |

---

## ⚠️ Avvertenze importanti

1. **Non committare segreti o tokens API** — se un giorno dovessi inserire chiavi, usa variabili d'ambiente esterne. I JSON nel repo sono solo config pubbliche/operative.
2. **I files di configurazione Ollama risiedono su disco locale** (`~/.pi/ollama-server-config.json`) e non nel repo; il repo contiene solo copie/reference delle configurazioni applicate.
3. Il backup dei JSON è consigliato prima di ogni modifica manuale: `updating_plan.md` spiega come fare.

---

*Configuraioni per Mac M4 48GB — s.priori@ifac.cnr.it — Luglio 2026*
