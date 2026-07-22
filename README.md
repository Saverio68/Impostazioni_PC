# Impostazioni_PC — Mac M4 48GB (Ollama & pi coding agent)

Questo repository gestisce le configurazioni e la documentazione per sincronizzare l'ambiente locale (**Ollama server** + **pi agent**) tramite il progetto "Impostazioni_PC". Non include il codice di applicazione, ma solo setup operativo.

## 📁 Struttura Files
```text
Impostazioni_PC/
├── settings.md           # Istruzioni originali (non modificare)
├── Readme.html           # Riepilogo visivo dinamico delle configurazioni
├── README.md             # Questo file
├── updating_plan.md      # Procedura manuale e script per gestire modelli Ollama
└── scripts/              # Script di automazione
    └── config-update.py  # Python script: rigenera JSON + HTML allineati a 'ollama ls'
```

## 🤖 Gestione Modelli e Automazione
Hai due opzioni per aggiornare le configurazioni dopo aver aggiunto o rimosso modelli da Ollama:

1. **Automatizzato (Raccomandato):** Esegui semplicemente `python3 scripts/config-update.py` dalla root della repo. Lo script rileterà `ollama list`, calcolerà i valori ottimali per il tuo Mac M4 48GB e sovrascriverà `Readme.html` e `~/.pi/agent/models.json`.
2. **Manuale:** Segui `updating_plan.md` per intervenire manualmente sui file JSON di configurazione e aggiornare la documentazione HTML a mano.

## 📘 Glossario Tecnico (Termini Configurazione)
I parametri qui definiti controllano l'inferenza su sessioni pesanti:

| Termine | Definizione tecnica | Valore attuale nel nostro setup |
|---|---|---|
| `num_predict` | Il "cappello" massimo di token scritti durante la generazione. | **65536**: impostato altissimo per evitare interruzioni premature (sopra 4096 default Ollama) su sessioni lunghe di coding. |
| `contextWindow` | Dimensione massima della memoria logica del modello. | **131k**: sfruttiamo l'hardware Mac M4 moderno per mantenere tutto il contesto in RAM. |
| `num_ctx` | Finestra attiva sulla GPU/Metal (effettivo costo in VRAM/RAM). | **65536** o uguale a num_predict. Calibrato per stabilità e velocità su 48GB unificati. |
| `temperature` | Creatività/Disperazione dei tokens generati. | **0.2** per Coding (sicuro), **0.5** per Vision (adattivo). |

## 🔑 Parametri chiave Ollama Server (`~/.pi/ollama-config.json`)
- **`f16_kv: true`**: Precisione 16-bit per la memoria delle chiavi (KV Cache). Fondamentale per stabilità su Mac M4.
- **`release_after_inference_delay_ms`**: Tempo di permanenza del modello in GPU prima di scaricarlo. Impostato a 60s per velocizzare switch rapidi tra task.

> 🧠 **Nota specifica su `num_predict`**: Se impostato basso (come il default Ollama), il modello si "zittirà" e fermerà la generazione anche se non ha finito il codice o la spiegazione logica. Su sessioni di lavoro lunghi, un valore alto è essenziale per integrità dell'output.

## ⚠️ Avvertenze Importanti
- **Non committare mai segreti** (API keys), né i pesanti files binari dei modelli (`~/.ollama/models/` è già escluso da `.gitignore`). I JSON sono solo riferimenti operativi.
- **RAM su Mac M4**: 48 GB Unificati. Questo ci permette di avere `num_ctx` enormi (65k+) che sui computer normali crasherebbero l'applicazione immediata.
